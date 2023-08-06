'''
Tests for :func:`pulmoscan.models.augmentation` module.
'''

import unittest

import tensorflow as tf

import pulmoscan.models.augmentation as augmentation

class ImageAugmentationTestCase(unittest.TestCase):
    '''
    Unit tests for :func:`augmentation.create_base_preprocessing_pipeline`
    function.
    '''

    @classmethod
    def setUpClass(cls):
        '''
        Set random seed for CI.
        '''

        super().setUpClass()
        tf.random.set_seed(1235435)

    def test_produces_same_outputs_at_test_and_reshapes_and_scales(self):
        '''
        Asserts that layer can be created, outputs has proper shape.
        Also asserts that image is scaled and resized.
        '''

        input_layer = tf.keras.layers.Input(shape=(224, 224, 3), dtype='float32')
        output_layer = augmentation.create_base_preprocessing_pipeline(
            input_layer,
            image_size=(100, 100),
            maximum_pixel_value=255.
        )
        model = tf.keras.Model(inputs=input_layer, outputs=output_layer)

        # pylint: disable=unexpected-keyword-arg
        input_batch = tf.random.uniform((2, 312, 312, 3), minval=0., maxval=255., dtype='float32')
        # pylint: enable=unexpected-keyword-arg

        output_first = model(input_batch, training=False)
        output_second = model(input_batch, training=False)
        self.assertEqual(tf.rank(output_first), 4)

        with self.subTest('Assert results match atevaluation'):
            self.assertTrue(
                tf.reduce_all(
                    tf.abs(output_first - output_second) < 1e-07
                )
            )

        with self.subTest('Test output is properly reshaped'):
            self.assertEqual(output_first.shape, (2, 100, 100, 3))

        with self.subTest('Assert maximum value is 1'):
            self.assertLessEqual(tf.reduce_max(output_first).numpy(), 1.)
