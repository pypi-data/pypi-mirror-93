import datetime
import enum
import json
import logging
import os
import sys
import typing

import gin
import numpy as np
import tensorflow as tf
from absl import app, flags

import pulmoscan.configurables  # pylint: disable=all
import pulmoscan.datasets.tagset as tagsets
from pulmoscan.datasets.base import DatasetSplit

FLAGS = flags.FLAGS

flags.DEFINE_string('config_file', None, "Path to experiment's config file.")
flags.DEFINE_string('base_experiment_folder', 'experiment', 'Location where all data will be stored.')
flags.DEFINE_bool('restore_from_checkpoint', False, 'If set, weights from latestcheckpoint will be loaded.')

physical_devices = tf.config.experimental.list_physical_devices('GPU')
print(f'Physical devices: {physical_devices}')
for x in physical_devices:
    print(f'Set memory growth for device: {x}')
    tf.config.experimental.set_memory_growth(x, True)


def maybe_create_project_folder(config_file: str, experiment_folder: str) -> str:
    base_name: str = os.path.basename(config_file)
    experiment_name, _ = os.path.splitext(base_name)
    folder_name = os.path.join(experiment_folder, experiment_name)
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)
    return folder_name


def _get_checkpoint_directory(experiment_directory) -> str:
    return os.path.join(experiment_directory, 'checkpoints')


def _create_tensorboard_callback(experiment_directory: str) -> tf.keras.callbacks.TensorBoard:
    tensorboard_path = os.path.join(experiment_directory, 'tensorboard')
    return tf.keras.callbacks.TensorBoard(tensorboard_path)


def _create_checkpoint_callback(experiment_directory: str) -> tf.keras.callbacks.ModelCheckpoint:
    checkpoint_dir = _get_checkpoint_directory(experiment_directory)
    checkpoint_path = os.path.join(checkpoint_dir, 'default')

    return tf.keras.callbacks.ModelCheckpoint(
        checkpoint_path, save_weights_only=True
    )


class ResultsLoggingMode(enum.Enum):
    TRAIN = enum.auto()
    EVAL = enum.auto()


def _log_results(
        history: typing.Mapping[str, typing.List[typing.Union[float, np.ndarray]]],
        mode: ResultsLoggingMode
    ):
    default_logger = logging.getLogger()
    results_as_dictionary = {}

    for metric_name, list_of_values in history.items():
        if mode == ResultsLoggingMode.TRAIN:
            if not metric_name.startswith('val_'):
                metric_name = 'train_' + metric_name
        elif mode == ResultsLoggingMode.EVAL:
            metric_name = 'test_' + metric_name
        else:
            raise ValueError(f'Unknown mode: {mode}')
        
        if isinstance(list_of_values, list):
            if len(list_of_values) == 0:
                raise ValueError('No metrics to long')

            if isinstance(list_of_values[0], np.ndarray):
                list_of_values = [typing.cast(np.ndarray, x).tolist() for x in list_of_values]

        results_as_dictionary[metric_name] = list_of_values

    default_logger.info(f'Results (mode {mode}):')
    default_logger.info(json.dumps(results_as_dictionary, indent=4, sort_keys=True))


def _log_config(experiment_directory: str):
    config_str = gin.config_str(max_line_length=256)
    with open(os.path.join(experiment_directory, 'config.cfg'), 'w') as file:
        file.write(config_str)


def _export_model(experiment_directory: str, model: tf.keras.Model):
    path_to_save: str = os.path.join(experiment_directory, 'model', 'saved_model')
    tf.saved_model.save(model, path_to_save)


def _log_tagset(experiment_directory: str, tagset_as_json: str):
    tagset_path: str = os.path.join(experiment_directory, 'tagset.json')
    with open(tagset_path, 'w', encoding='utf-8') as tagset_file:
        tagset_file.write(tagset_as_json)


def _log_summary(experiment_directory: str, model: tf.keras.Model):
    with open(os.path.join(experiment_directory, 'summary.txt'), 'w') as summary_file:
        model.summary(print_fn=lambda x: summary_file.write(x + '\n'))


@gin.configurable(denylist=['restore_from_checkpoint'])
def train_experiment(
        experiment_directory: str,
        model_factory: typing.Optional[typing.Callable[[int], tf.keras.Model]] = None,
        dataset_cls: typing.Optional[typing.Callable[..., tf.data.Dataset]] = None,
        global_tagset: typing.Optional[tagsets.GlobalTagset] = None,
        total_train_steps: int = 500,
        steps_per_epoch: int = 500,
        callbacks_for_train: typing.Optional[typing.List[tf.keras.callbacks.Callback]] = None,
        validation_steps: int = 10000,
        validation_freq: int = 1,
        test_steps: int = 1000,
        append_default_callbacks: bool = True,
        restore_from_checkpoint: bool = False
    ):
    assert model_factory is not None
    assert dataset_cls is not None
    assert global_tagset is not None

    if callbacks_for_train is None:
        callbacks_for_train = list()

    callbacks_for_train.append(
        tf.keras.callbacks.LambdaCallback(on_train_begin=lambda _: _log_config(experiment_directory))
    )
    callbacks_for_train.append(
        tf.keras.callbacks.LambdaCallback(
            on_train_begin=lambda _: _log_tagset(experiment_directory, json.dumps(global_tagset.to_dict()))
        )
    )

    if append_default_callbacks:
        callbacks_for_train += [
            _create_tensorboard_callback(experiment_directory),
            _create_checkpoint_callback(experiment_directory)
        ]

    model = model_factory(len(global_tagset))
    dataset = dataset_cls()
    train_dataset = dataset(DatasetSplit.TRAIN)
    val_dataset = dataset(DatasetSplit.VAL)

    callbacks_for_train.append(
        tf.keras.callbacks.LambdaCallback(
            on_train_end=lambda _: _log_summary(experiment_directory, model)
        )
    )

    if restore_from_checkpoint:
        checkpoint_dir = _get_checkpoint_directory(experiment_directory)
        checkpoint = tf.train.latest_checkpoint(checkpoint_dir)
        model.load_weights(checkpoint)

    if steps_per_epoch > total_train_steps:
        raise ValueError(f'Number of steps per epoch is greater than total number of steps')

    #: if total_train_steps mode steps_per_epoch > 0 then the module is removed from
    #: total train steps

    epochs: int = total_train_steps // steps_per_epoch
    history = model.fit(
        train_dataset, epochs=epochs, steps_per_epoch=steps_per_epoch, callbacks=callbacks_for_train,
        validation_data=val_dataset, validation_steps=validation_steps, validation_freq=validation_freq
    ).history
    _log_results(history, ResultsLoggingMode.TRAIN)

    test_dataset = dataset(DatasetSplit.TEST)
    evaluation_results = model.evaluate(
        test_dataset, steps=test_steps, return_dict=True, callbacks=callbacks_for_train
    )
    _log_results(evaluation_results, ResultsLoggingMode.EVAL)
    
    _export_model(experiment_directory, model)


def _setup_logger(experiment_directory: str, minimum_logging_level = logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(minimum_logging_level)
    formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

    stdout_handler = logging.StreamHandler(sys.stdout)
    stdout_handler.setLevel(minimum_logging_level)
    stdout_handler.setFormatter(formatter)

    time = "{:%Y_%m_%d_%H_%M_%S}".format(datetime.datetime.now())
    file_name: str = f'log_{time}.log'
    file_name = os.path.join(experiment_directory, file_name)
    file_handler = logging.FileHandler(file_name, mode='w')
    file_handler.setLevel(minimum_logging_level)
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stdout_handler)


def main(argv):
    del argv

    config_file: str = FLAGS.config_file
    base_experiment_folder: str = FLAGS.base_experiment_folder
    should_restore_from_checkpoint: bool = FLAGS.restore_from_checkpoint

    gin.parse_config_file(config_file)

    experiment_directory = maybe_create_project_folder(config_file, base_experiment_folder)
    _setup_logger(experiment_directory)
    train_experiment(experiment_directory, restore_from_checkpoint=should_restore_from_checkpoint)


def entry():
    '''
    An entrypoint for command line tool.
    '''
    app.run(main)


if __name__ == '__main__':
    entry()
