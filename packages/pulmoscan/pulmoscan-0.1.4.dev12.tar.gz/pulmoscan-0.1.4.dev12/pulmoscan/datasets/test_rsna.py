'''
Contains test for :func:`pulmoscan.datasets.rsna` module.
'''


import unittest
import unittest.mock

import numpy as np
import gin
import tensorflow as tf

import pulmoscan.datasets.base as base
import pulmoscan.datasets.rsna as rsna
import pulmoscan.datasets.tagset as tagsets


class RsnaPatientToDiagnoseTestCase(unittest.TestCase):
    '''
    Unit tests for :func:`rsna.RsnaPatientToDiagnose` class.
    '''

    CSV_PATH: str = 'resources/test/rsna/rsna_patient_to_label_test.csv'
    REQUESTS = [
        '0004cfab-14fd-4e49-80ba-63a80b6bddd6', '00313ee0-9eaa-42f4-b0ab-c148ed3241cd',
        '00322d4d-1c29-4943-afc9-b6754be640eb', '003d8fa0-6bf1-40ed-b54c-ac657f8495c5',
        '113d8fa0-6bf1-40ed-b54c-ac657f8495c5', '98755ttt-6bf1-40ed-b54c-ac657f8495c5',
        '00436515-870c-4b36-a041-de91049b9ab4', 'fsdgfdsf-870c-4b36-a041-fsdfsd9ab4',
        '12323dsf-870c-4b36-a041-fsdfsd9ab4', 'qwerty11-870c-4b36-a041-fsdfsd9ab4'
    ]

    def test_create(self):
        '''
        Test just the creation
        '''

        rsna.RsnaPatientToDiagnose(
            self.CSV_PATH, val_size=0.25, test_size=0.25, tagset=tagsets.build_global_tagset()
        )

    def test_splitting_for_train_dev_test(self):
        '''
        Test number of training samples per split.
        '''

        mapping = rsna.RsnaPatientToDiagnose(
            self.CSV_PATH, val_size=0.25, test_size=0.25, tagset=tagsets.build_global_tagset()
        )
        self.assertEqual(len(mapping.get_patients_for_split(base.DatasetSplit.TRAIN)), 4)
        self.assertEqual(len(mapping.get_patients_for_split(base.DatasetSplit.VAL)), 2)
        self.assertEqual(len(mapping.get_patients_for_split(base.DatasetSplit.TEST)), 2)

    def test_patient_to_diagnose(self):
        '''
        Test if mapping is performed correctly.
        '''

        mapping = rsna.RsnaPatientToDiagnose(
            self.CSV_PATH, val_size=0.25, test_size=0.25, tagset=tagsets.build_global_tagset()
        )
        ref_responces = [
            'No Lung Opacity / Not Normal', 'No Lung Opacity / Not Normal',
            'Normal', 'Normal', 'Normal', 'Normal', 'Lung Opacity', 'Lung Opacity',
            'Lung Opacity', 'Lung Opacity'
        ]
        self.assertEqual(len(self.REQUESTS), len(ref_responces))
        for i, (request, response) in enumerate(zip(self.REQUESTS, ref_responces)):
            if i in (0, 1):
                with self.assertRaises(ValueError):
                    mapping.patient_to_diagnose(request)
                continue
            self.assertEqual(mapping.patient_to_diagnose(request), response)


class RsnaGeneratorTestCase(unittest.TestCase):
    '''
    Unit tests for :func:`rsna.RsnaGenerator` class.
    '''

    DICOM_DIR: str = 'resources/test/rsna/dicoms'
    CSV_PATH: str = 'resources/test/rsna/rsna_patient_to_label_test.csv'
    IMAGE_SIZE = (123, 456)

    @classmethod
    def setUpClass(cls):
        '''
        Gin-configure some parameters for simplicity.
        '''

        gin.bind_parameter('RsnaPatientToDiagnose.csv_with_labels_path', cls.CSV_PATH)
        gin.bind_parameter('RsnaPatientToDiagnose.test_size', 0.25)
        gin.bind_parameter('RsnaPatientToDiagnose.val_size', 0.25)
        gin.bind_parameter('RsnaPatientToDiagnose.tagset', tagsets.build_global_tagset())

        gin.bind_parameter('RsnaGenerator.dataset_split', base.DatasetSplit.TRAIN)
        gin.bind_parameter('RsnaGenerator.image_target_size', cls.IMAGE_SIZE)

        gin.bind_parameter('RsnaDataset.target_image_shape', cls.IMAGE_SIZE)
        gin.bind_parameter('RsnaDataset.number_of_channels', 1)

    @classmethod
    def tearDownClass(cls):
        '''
        Clear configs.
        '''

        gin.clear_config()

    def setUp(self):
        '''
        Re-create tagset before each test.
        '''

        self._tagset: tagsets.GlobalTagset = tagsets.build_global_tagset()

    def test_create_generator(self):
        '''
        Test just the creation.
        '''

        rsna.RsnaGenerator(self.DICOM_DIR, self._tagset, self.IMAGE_SIZE)

    def test_iterate_test_dataset(self):
        '''
        Iterate for a couple of steps and check output types.
        '''

        generator = rsna.RsnaGenerator(self.DICOM_DIR, self._tagset, self.IMAGE_SIZE)
        i = 0
        for i, (image, diagnose_id) in enumerate(generator()):
            self.assertIsInstance(image, np.ndarray)
            self.assertEqual(len(image.shape), 3)

            self.assertEqual(image.shape[-1], 1)
            self.assertEqual(image.shape[:-1], self.IMAGE_SIZE[::-1])
            self.assertIsInstance(diagnose_id, int)
        self.assertEqual(i, 1) # There are 3 out-of-tagset objects


def sample_generator():
    '''
    Sample generator for simple testing.
    '''

    yield from [
        (np.ones((250, 120, 3), 'float32'), 1),
        (np.ones((250, 120, 3), 'float32'), 0),
        (np.ones((250, 120, 3), 'float32'), 1)
    ]


class RsnaTFDatasetTestCase(unittest.TestCase):
    '''
    Contains unit tests for :func:`rsna.RsnaDataset` class.
    '''

    def test_mock_of_generator(self):
        '''
        Test if mocking behaves in an expected way.
        '''

        data = list(sample_generator())
        self.assertEqual(len(data), 3)
        for image, label in data:
            self.assertIsInstance(image, np.ndarray)
            self.assertIsInstance(label, int)

    def test_train_split(self):
        '''
        Runs test for train split. Check ranks and shapes.
        '''

        dataset = rsna.RsnaDataset(
            batch_size=2,
            drop_remainder=False,
            train_generator=sample_generator,
            target_image_shape=(250, 120),
            number_of_channels=3
        )
        tf_dataset = dataset(base.DatasetSplit.TRAIN)
        self.assertIsInstance(tf_dataset, tf.data.Dataset)

        n_batches = 0
        for images, labels in tf_dataset.take(5).as_numpy_iterator():
            n_batches += 1
            self.assertEqual(tf.rank(images), 4)
            self.assertEqual(tf.rank(labels), 1)

            self.assertEqual(tf.shape(images)[0], tf.shape(labels)[0])
            self.assertEqual(tf.shape(images)[0], 2)
            self.assertTrue(tf.reduce_all(tf.shape(images)[1:] == (250, 120, 3)))

        self.assertEqual(n_batches, 5)
