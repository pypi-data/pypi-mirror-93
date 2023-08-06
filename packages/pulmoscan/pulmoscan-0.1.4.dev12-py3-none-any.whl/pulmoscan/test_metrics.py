'''
Unit-tests for :func:`pulmoscan.metrics` module.
'''

import unittest

import numpy.testing
import sklearn
import sklearn.metrics
import tensorflow as tf

import pulmoscan.metrics as metrics


class BinaryTestCase(unittest.TestCase):
    '''
    Unit-tests for metrics at binary classification.
    '''

    NUM_CLASSES = 2

    @property
    def y_true(self):
        '''
        Getter for test gt labels.
        '''

        return tf.convert_to_tensor([0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0], 'int32')

    @property
    def y_pred(self):
        '''
        Getter for predicted labels in one-hot labels.
        '''

        return tf.one_hot([0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1], self.NUM_CLASSES, on_value=1, off_value=0)

    @property
    def y_pred_sparse(self):
        '''
        Getter for predicted labels in sparse format.
        '''

        return tf.argmax(self.y_pred, -1)

    def setUp(self):
        '''
        Setup metrics.
        '''

        self._precision = metrics.VectorPrecision(self.NUM_CLASSES)
        self._recall = metrics.VectorRecall(self.NUM_CLASSES)
        self._f1_score = metrics.VectorF1(self.NUM_CLASSES)

        self._precision.update_state(self.y_true, self.y_pred)
        self._recall.update_state(self.y_true, self.y_pred)
        self._f1_score.update_state(self.y_true, self.y_pred)

    def test_equal_lengths(self):
        '''
        Sanity check for getters.
        '''

        self.assertEqual(len(self.y_true), len(self.y_pred))

    def test_binary_classification_precision(self):
        '''
        Test for precision in the case of binary classification.
        '''

        ref_precision = sklearn.metrics.precision_recall_fscore_support(
            self.y_true, self.y_pred_sparse
        )[0]
        numpy.testing.assert_array_almost_equal(ref_precision, self._precision.result().numpy())

    def test_binary_classification_recall(self):
        '''
        Test for recall in the case of binary classification.
        '''

        ref_recall = sklearn.metrics.precision_recall_fscore_support(
            self.y_true, self.y_pred_sparse
        )[1]
        numpy.testing.assert_array_almost_equal(ref_recall, self._recall.result().numpy())

    def test_binary_classification_f1(self):
        '''
        Test for f1 score in the case of binary classification.
        '''

        ref_f1 = sklearn.metrics.precision_recall_fscore_support(
            self.y_true, self.y_pred_sparse
        )[2]
        numpy.testing.assert_array_almost_equal(ref_f1, self._f1_score.result().numpy())
