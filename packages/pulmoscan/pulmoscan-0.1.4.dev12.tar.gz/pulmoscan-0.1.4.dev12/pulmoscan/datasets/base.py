'''
Contains base classes and commonly-used utilities for datasets.
'''

import abc
import enum
import typing
import gin
import tensorflow as tf


@gin.constants_from_enum
class DatasetSplit(enum.Enum):
    '''
    Determines the split of the dataset.
    '''

    TRAIN = enum.auto()
    VAL = enum.auto()
    TEST = enum.auto()


class BaseDatasetGenerator(abc.ABC):
    '''
    Abstract class for generator instances.
    '''

    @abc.abstractmethod
    def __call__(self) -> typing.Generator:
        raise NotImplementedError('Not implemented in base class')


class BaseTFDataset(abc.ABC):
    """Base class for Tensorflow wrappers for dataset.
    Supports splitting dataset into train-dev-test parts.

    Args:
        train_generator (Optional[BaseDatasetGenerator], optional): An instance of
            :func:`BaseDatasetGenerator` for train split.
        val_generator (Optional[BaseDatasetGenerator], optional): An instance of
            :func:`BaseDatasetGenerator` for validation split.
        test_generator (Optional[BaseDatasetGenerator], optional): An instance of
            :func:`BaseDatasetGenerator` for test split.
    """

    def __init__(
            self,
            train_generator: typing.Optional[BaseDatasetGenerator] = None,
            val_generator: typing.Optional[BaseDatasetGenerator] = None,
            test_generator: typing.Optional[BaseDatasetGenerator] = None
        ):
        self._train_gen = train_generator
        self._val_gen = val_generator
        self._test_gen = test_generator

    def _get_generator_for_split(self, split: DatasetSplit) -> typing.Optional[BaseDatasetGenerator]:
        '''
        Returns generator for runtime-requested split.
        '''

        if split == DatasetSplit.TRAIN:
            return self._train_gen
        if split == DatasetSplit.VAL:
            return self._val_gen
        if split == DatasetSplit.TEST:
            return self._test_gen
        raise ValueError(f'Split {split} is not recognized.')

    @abc.abstractmethod
    def __call__(self, split: DatasetSplit) -> tf.data.Dataset:
        raise NotImplementedError('Not implemented in base class.')
