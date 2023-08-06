'''
Utils that are common for most of models.
'''

import typing

import gin
import tensorflow as tf

import pulmoscan.constants as constants
import pulmoscan.datasets.tagset as tagsets
import pulmoscan.metrics as custom_metrics
import pulmoscan.models.augmentation as augmentation


ImageEncoderClass = typing.Union[typing.Type[tf.keras.Model], typing.Type[tf.keras.layers.Layer]]

#pylint: disable=too-many-locals
@gin.configurable
def create_model(
        number_of_classes: int,
        image_encoder_cls: typing.Optional[ImageEncoderClass] = None,
        use_augmentation: bool = True,
        input_image_size: typing.Optional[typing.Tuple[int]] = None,
        n_input_channels: int = 1,
        tagset: typing.Optional[tagsets.GlobalTagset] = None
    ) -> tf.keras.Model:
    """Returns a compiled model for classification as Keras model.

    Args:
        number_of_classes (int): Number of classes to predict.
        image_encoder_cls (Optional[ImageEncoderClass]): Callable that returns model or layer
            for encoding an image. It may be class of Keras layer itself.
            Image encoder must return a feature map with shape ``[h, w, c]``.
        use_augmentation (bool): If ``True`` then augmentation model is inserted.
        input_image_size (Optional[Tuple[int]]): Input size for images as tuple.
            Should contain only 2 numbers. Channels dimensionality is passed separately.
        n_input_channels (int): Number of dimensions in input images.
        tagset (Optional[tagsets.GlobalTagset]): An instance of GlobalTagset class to create per-class
            metrics.

    Raises:
        ValueError: "input_image_size" is missing.

    Returns:
        tf.keras.Model: compiled keras model.
    """

    if input_image_size is None:
        raise ValueError('Expected "input_image_size" argument, got None')

    if tagset is None:
        raise ValueError('Gin-configure "tagset" argument for "create_lenet_model" function.')

    if image_encoder_cls is None:
        raise ValueError('Gin-configure "image_encoder_cls" argument for "create_lenet_model" function.')

    image_input = tf.keras.layers.Input(shape=(*input_image_size, n_input_channels), dtype='float32')
    feature_map = image_input
    if use_augmentation:
        feature_map = augmentation.create_base_preprocessing_pipeline(feature_map)

    feature_map = image_encoder_cls()(feature_map)
    visualization_output = feature_map

    feature_map = tf.keras.layers.GlobalAveragePooling2D()(feature_map)
    clf_layer = tf.keras.layers.Dense(number_of_classes, name='prediction')
    logits = clf_layer(feature_map)

    class_weights = clf_layer.get_weights()[0]
    visualization_output = tf.matmul(visualization_output, class_weights)

    model = tf.keras.Model(
        inputs=image_input,
        outputs={
            constants.LOGITS_OUTPUT: logits,
            constants.VISUALIZATION_OUTPUT: visualization_output
        }
    )

    return compile_with_default_metrics(model, number_of_classes)


@gin.configurable(whitelist=['optimizer_cls', 'learning_rate', 'user_provided_metrics', 'tagset'])
def compile_with_default_metrics(
        model: tf.keras.Model,
        number_of_classes: int,
        optimizer_cls: tf.keras.optimizers.Optimizer = tf.keras.optimizers.Adam,
        learning_rate: typing.Union[float, tf.keras.optimizers.schedules.LearningRateSchedule] = 1e-03,
        user_provided_metrics: typing.Optional[typing.List[tf.keras.metrics.Metric]] = None,
        tagset: typing.Optional[tagsets.GlobalTagset] = None
    ) -> tf.keras.Model:
    """Base actions that take place at model compiling: creation of metrics and
    setting up loss function and tokenizer.

    Args:
        model (tf.keras.Model): Keras model to compile.
        number_of_classes (int): Total number of classes for classificationtask.
        optimizer_cls (tf.keras.optimizers.Optimizer, optional): Class of optimizer to be
            used for compiling. Defaults to Adam optimizer.
        learning_rate (Union[float, tf.keras.optimizers.schedules.LearningRateSchedule], optional):
            Initial learining rate for training. Could be a float or a learning rate schedule.
        user_provided_metrics (Optional[typing.List[tf.keras.metrics.Metric]], optional):
            List of Keras metrics to compile with.
        tagset (Optional[tagsets.GlobalTagset], optional): An instance of GlobalTagset class
            to create per-class metrics.

    Returns:
        tf.keras.Model: Compiled model.
    """

    if tagset is None:
        raise ValueError('Gin-configure argument "tagset" for function "compile_with_default_metrics"')

    if user_provided_metrics is None:
        user_provided_metrics = list()

    metrics = user_provided_metrics
    metrics.extend(typing.cast(typing.List[object], ['sparse_categorical_accuracy']))

    for label in tagset.labels:
        label_id: int = tagset.convert_global_to_id(label)

        metrics.extend([
            custom_metrics.ClassPrecision(number_of_classes, label_id, label.lower() + '_precision'),
            custom_metrics.ClassRecall(number_of_classes, label_id, label.lower() + '_recall'),
            custom_metrics.ClassF1(number_of_classes, label_id, label.lower() + '_f1')
        ])

    metrics_as_dict = {
        constants.LOGITS_OUTPUT: metrics,
        constants.VISUALIZATION_OUTPUT: []
    }
    losses = {
        constants.LOGITS_OUTPUT: tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
        constants.VISUALIZATION_OUTPUT: None
    }
    model.compile(
        optimizer=optimizer_cls(learning_rate),
        loss=losses,
        metrics=metrics_as_dict
    )
    return model
