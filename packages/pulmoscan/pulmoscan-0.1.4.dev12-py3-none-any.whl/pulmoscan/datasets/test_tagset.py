'''
Contains a set of unit tests for :func:`pulmoscan.datasets.tagset` module.
'''


import unittest
import typing
import os
import tempfile
import shutil

import pulmoscan.datasets.tagset as tagsets


class UnionTagsetsTestCase(unittest.TestCase):
    '''
    Unit tests for :func:`tagsets.union_tagsets` and related functions.
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Create toy mappings for testing.
        '''

        super().setUpClass()
        cls._temp_folder: str = tempfile.mkdtemp()
        cls._first_mapping_path: str = os.path.join(cls._temp_folder, 'first.txt')
        cls._second_mapping_path: str = os.path.join(cls._temp_folder, 'second.txt')
        cls._duplicate_with_conflict: str = os.path.join(cls._temp_folder, 'conflict.txt')

        with open(cls._first_mapping_path, 'w') as file:
            file.write('Normal;Normal\n')
            file.write('Lung Opacity;Pneumonia\n')

        with open(cls._second_mapping_path, 'w') as file:
            file.write('Normal;Normal\n')
            file.write('Not Normal;Anomaly')

        with open(cls._duplicate_with_conflict, 'w') as file:
            file.write('Lung Opacity;Anomaly')

    @classmethod
    def tearDownClass(cls):
        '''
        Remove all temp files.
        '''

        super().tearDownClass()
        shutil.rmtree(cls._temp_folder)

    def test_read_map_first(self):
        '''
        Assert that the first mapping is read correctly.
        '''

        mapping = tagsets._read_map(self._first_mapping_path) # pylint: disable=protected-access
        self.assertIsInstance(mapping, typing.Mapping)
        self.assertDictEqual(dict(mapping), {
            'Normal': 'Normal',
            'Lung Opacity': 'Pneumonia'
        })

    def test_read_map_second(self):
        '''
        Assert that the second mapping is read correctly.
        '''

        mapping = tagsets._read_map(self._second_mapping_path) # pylint: disable=protected-access
        self.assertIsInstance(mapping, typing.Mapping)
        self.assertDictEqual(dict(mapping), {
            'Normal': 'Normal',
            'Not Normal': 'Anomaly'
        })

    def test_read_map_that_contains_error(self):
        '''
        Assert that the third mapping (with logical error) is read correctly.
        '''

        mapping = tagsets._read_map(self._duplicate_with_conflict) # pylint: disable=protected-access
        self.assertIsInstance(mapping, typing.Mapping)
        self.assertDictEqual(dict(mapping), {
            'Lung Opacity': 'Anomaly'
        })

    def test_union_two_regular_mappings(self):
        '''
        Test that two mappings with no errors could be joined.
        '''

        tagset = tagsets.union_tagsets([self._first_mapping_path, self._second_mapping_path])
        self.assertIsInstance(tagset, tagsets.GlobalTagset)

        self.assertEqual(len(tagset), 3)
        ids = [tagset.convert_local_to_id(x) for x in ['Normal', 'Not Normal', 'Lung Opacity']]
        self.assertListEqual(sorted(ids), [0, 1, 2])

    def test_union_raises_error_at_duplications(self):
        '''
        Test that union with a mapping that contains a logical error raises an exception.
        '''

        with self.assertRaises(KeyError):
            tagsets.union_tagsets([self._first_mapping_path, self._second_mapping_path, self._duplicate_with_conflict])


class GlobalTagsetTestCase(unittest.TestCase):
    '''
    Contains test cases for :func:`tagsets.GlobalTagset`.
    '''

    def test_compare_to_dictionary(self):
        '''
        Build global tagset and check everything is present.
        '''

        glob = tagsets.build_global_tagset()
        self.assertIsInstance(glob, tagsets.GlobalTagset)
        self.assertEqual(len(glob), 2)
        self.assertIn('Lung Opacity', glob)
        self.assertIn('Normal', glob)
