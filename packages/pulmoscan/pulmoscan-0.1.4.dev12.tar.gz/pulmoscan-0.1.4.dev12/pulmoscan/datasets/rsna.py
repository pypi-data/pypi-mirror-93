'''
Contains tools concerning RSNA dataset.
'''


import typing
import os

import cv2
import gin
import numpy as np
import pandas as pd
import tensorflow as tf
import sklearn.model_selection

import pulmoscan.datasets.base as base
import pulmoscan.datasets.tagset as tagsets
import pulmoscan.parse.image as image_utils


# pylint: disable=too-many-instance-attributes
@gin.configurable
class RsnaPatientToDiagnose:
    """Implements the process of retrieving classification labels for patients.

    Args:
        csv_with_labels_path (Optional[str], optional): Path to the csv file with 2 columns:
            * ``patientID`` - identifier of the patient
            * ``class`` - target label to predict
        val_size (float): Relative size of validation part.
        test_size (float): Relative size of test part.
        random_seed (int): For the possibility to reproduce results.

    Raises:
        ValueError: if path is not provided
    """
    # TODO: DROP RECORDS WHICH CLASS IS NOT IN GLOBAL TAGSET

    def __init__(
            self,
            csv_with_labels_path: typing.Optional[str] = None,
            tagset: typing.Optional[tagsets.GlobalTagset] = None,
            val_size: float = 0.1,
            test_size: float = 0.2,
            random_seed: int = 1234
        ):
        if csv_with_labels_path is None:
            raise ValueError('Gin-configure "csv_with_labels_path" argument')
        if tagset is None:
            raise ValueError('Gin-configure "tagset" argument')

        np.random.seed(random_seed)

        self._csv_with_labels: str = csv_with_labels_path
        self._random_seed: int = random_seed
        self._val_size: float = val_size
        self._test_size: float = test_size
        self._tagset: tagsets.GlobalTagset = tagset
        self._patient_to_class_name: typing.MutableMapping[str, str] = {}

        self._train_patients: typing.List[str]
        self._val_patients: typing.List[str]
        self._test_patients: typing.List[str]

        self.__read_dataframe_and_perform_splits()
        self.__assert_no_intersections()

    def __read_dataframe_and_perform_splits(self):
        '''
        Reads dataframe with patient-class mapping and performs
        stratified splitting into train, val and test.
        '''

        dataframe: pd.DataFrame = pd.read_csv(self._csv_with_labels)
        dataframe = dataframe.drop_duplicates()
        mask_in_tagset = dataframe['class'].map(lambda x: not x in self._tagset)
        dataframe = dataframe.drop(dataframe[mask_in_tagset].index)

        for patient_id, class_name in zip(dataframe['patientId'], dataframe['class']):
            self._patient_to_class_name[patient_id] = class_name

        train, val_and_test = sklearn.model_selection.train_test_split(
            dataframe, test_size=self._val_size + self._test_size, random_state=self._random_seed,
            stratify=dataframe['class']
        )

        new_test_size = self._test_size / (self._test_size + self._val_size)
        val, test = sklearn.model_selection.train_test_split(
            val_and_test, test_size=new_test_size, random_state=self._random_seed + 15,
            stratify=val_and_test['class']
        )
        self._train_patients = list(train['patientId'])
        self._val_patients = list(val['patientId'])
        self._test_patients = list(test['patientId'])

    def __assert_no_intersections(self):
        '''
        Assert that splits for not overlap by patients
        '''

        assert len(set(self._train_patients).intersection(set(self._val_patients))) == 0
        assert len(set(self._train_patients).intersection(set(self._test_patients))) == 0
        assert len(set(self._test_patients).intersection(set(self._val_patients))) == 0

    def get_patients_for_split(self, split: base.DatasetSplit) -> typing.List[str]:
        """Returns a list of patients for the requested split.

        Args:
            split (DatasetSplit): Required split.

        Returns:
            typing.List[str]: List of patient ids for the split.
        """

        if split == base.DatasetSplit.TRAIN:
            return self._train_patients
        if split == base.DatasetSplit.VAL:
            return self._val_patients
        if split == base.DatasetSplit.TEST:
            return self._test_patients
        raise ValueError(f'Unrecognized split: {split}')

    def patient_to_diagnose(self, patient_id: str) -> str:
        """Convert patinet`s id to diagnose string label.

        Args:
            patient_id (str): identifier of a patient. Comes from the csv file from the
                dataset.

        Raises:
            ValueError: There is no label for patient.

        Returns:
            str: Diagnose label as string.
        """

        if patient_id not in self._patient_to_class_name:
            raise ValueError(f'There is no labels for patient with patientId={patient_id}')
        return self._patient_to_class_name[patient_id]


@gin.configurable
class RsnaGenerator(base.BaseDatasetGenerator):
    """Main generator of training examples for RSNA dataset.

    Args:
        dcm_root_directory (Optional[str], optional): Root directory with DCM files for the
            current dataset split (train/test/dev). All dicoms from that folders are considered
            to belong to one split.
        tagset (Optional[tagsets.GlobalTagset], optional): Tagset instance for converting global
            diagnose labels to integers.
        image_target_size (Optional[Tuple[int, int]]): Reshape each image to that size.
        dataset_split (Optional[DatasetSplit]): See :func:`DatasetSplit` for details.

    Raises:
        ValueError: Any parameter is not gin-configured.
        FileNotFoundError: root directory with dicoms is missing.
        FileExistsError: not a directory.
    """

    def __init__(
            self,
            dcm_root_directory: typing.Optional[str] = None,
            tagset: typing.Optional[tagsets.GlobalTagset] = None,
            image_target_size: typing.Optional[typing.Tuple[int, int]] = None,
            dataset_split: typing.Optional[base.DatasetSplit] = None
        ):
        super().__init__()
        if dcm_root_directory is None:
            raise ValueError('Gin-configure "dcm_root_directory" argument')
        if tagset is None:
            raise ValueError('Gin-configure "tagset" argument')
        if image_target_size is None:
            raise ValueError('Gin-configure "image_target_size" argument.')
        if dataset_split is None:
            raise ValueError('Gin-configure "dataset_split" argument')

        if not os.path.exists(dcm_root_directory):
            raise FileNotFoundError('RSNA directory with dicoms doesnt exist')
        if not os.path.isdir(dcm_root_directory):
            raise FileExistsError('Provided path for RSNA is not a directory')

        self._root_dir: str = dcm_root_directory
        self._tagset: tagsets.GlobalTagset = tagset
        self._target_image_size: typing.Tuple[int, int] = image_target_size
        self._patient_to_diagnose: RsnaPatientToDiagnose = RsnaPatientToDiagnose()
        self._dataset_split: base.DatasetSplit = dataset_split

    def __call__(self) -> typing.Generator[typing.Tuple[np.ndarray, int], None, None]:
        '''
        Iterate all training examples and yield image and class label for each of them.
        '''

        patients_for_current_split = set(self._patient_to_diagnose.get_patients_for_split(
            self._dataset_split
        ))

        for file_name in os.listdir(self._root_dir):
            file_path: str = os.path.join(self._root_dir, file_name)
            patient_id: str = os.path.splitext(file_name)[0]
            if patient_id not in patients_for_current_split:
                continue

            pil_image = image_utils.extract_image(file_path)
            pil_image = pil_image.resize(self._target_image_size)
            image_as_array = cv2.equalizeHist(np.array(pil_image)) # pylint: disable=no-member

            diagnose: str = self._patient_to_diagnose.patient_to_diagnose(patient_id)
            if diagnose not in self._tagset:
                continue
            diagnose_id: int = self._tagset.convert_local_to_id(diagnose)

            yield image_as_array[:, :, None], diagnose_id


@gin.configurable
class RsnaDataset(base.BaseTFDataset):
    """tf.data.Dataset wrapper for generator. Implements splitting mechanism.

    Args:
        batch_size (int, optional): Size of batches to create.
        drop_remainder (bool, optional): If ``True`` and dataset`s size is not divisible by
            ``batch_size``, the rest of training samples will be dropped.
        target_image_shape (Optional[Tuple[int, int]]): Sizes of images.
        number_of_channels (int): Number of channels each image has.
        train_generator (Optional[RsnaGenerator], optional): RsnaGenerator instance for traninig
            split.
        val_generator (Optional[RsnaGenerator], optional): RsnaGenerator instance for validation
            split.
        test_generator (Optional[RsnaGenerator], optional): RsnaGenerator instance for test
            split.
    """

    PREFETCH_BUFFER_SIZE: int = 64
    SHUFFLE_BUFFER_SIZE: int = 1024

    def __init__(
            self,
            batch_size: int = gin.REQUIRED,
            target_image_shape: typing.Tuple[int, int] = None,
            number_of_channels: int = 1,
            drop_remainder: bool = False,
            train_generator: typing.Optional[RsnaGenerator] = None,
            val_generator: typing.Optional[RsnaGenerator] = None,
            test_generator: typing.Optional[RsnaGenerator] = None
        ):
        super().__init__(train_generator, val_generator, test_generator)

        if target_image_shape is None:
            raise ValueError('Gin-configure "target_image_shape" for RsnaDataset')

        self._batch_size: int = batch_size
        self._target_image_shape = target_image_shape
        self._number_of_channels = number_of_channels
        self._drop_remainder = drop_remainder

    def __call__(self, split: base.DatasetSplit) -> tf.data.Dataset:
        """
        Creates tf.data.Dataset for the requested split.
        """

        generator = self._get_generator_for_split(split)
        if generator is None:
            raise ValueError(f'Configure rsna generator for split {split}')

        generator = typing.cast(RsnaGenerator, generator)
        dataset = tf.data.Dataset.from_generator(
            generator, output_types=('float32', 'int32'),
            output_shapes=((*self._target_image_shape, self._number_of_channels), ()) # type: ignore
        )

        if split == base.DatasetSplit.TRAIN:
            dataset = dataset.repeat().shuffle(self.SHUFFLE_BUFFER_SIZE)

        dataset = dataset.batch(self._batch_size, drop_remainder=self._drop_remainder)
        dataset = dataset.prefetch(self.PREFETCH_BUFFER_SIZE)
        return dataset
