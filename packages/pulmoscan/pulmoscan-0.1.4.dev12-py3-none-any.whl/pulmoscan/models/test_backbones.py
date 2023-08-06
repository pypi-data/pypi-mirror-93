'''
Contains tests for models from :func:`pulmoscan.layers.image_encoders` module.
'''

import unittest

import tensorflow as tf

import pulmoscan.models.backbones as backbones

GPU_DEVICES = list(tf.config.list_physical_devices('GPU'))

class GrayToRGBTestCase(unittest.TestCase):
    def test_converts_batch_with_axis(self):
        batch = tf.random.uniform((1, 12, 12, 1), 0, 1, 'float32') # pylint: disable=all
        output = backbones.grayscale_batch_to_rgb(batch)
        self.assertEqual(tf.rank(output), 4)
        self.assertEqual(output.shape, (1, 12, 12, 3))

class AlexNetTestCase(unittest.TestCase):
    '''
    Tests for :func:`backbones.AlexNet` class.
    '''

    def test_can_create_and_pass(self):
        '''
        Main test.
        '''

        model = backbones.AlexNet()
        inputs = tf.random.uniform((1, 227, 227, 3), minval=0., maxval=1., dtype='float32') # pylint: disable=unexpected-keyword-arg
        outputs = model(inputs)
        self.assertTrue(tf.is_tensor(outputs))
        self.assertEqual(tf.rank(outputs), 4)


class KerasApplicationsBackbonesTestCase(unittest.TestCase):
    '''
    Base unit tests for encoders forked from Keras.
    '''

    def get_input_batch(self, is_grayscale: bool):
        '''
        Getter for default input batch.
        '''

        last_dim = 1 if is_grayscale else 3
        return tf.random.uniform((1, 112, 112, last_dim), minval=0, maxval=255, dtype='float32') # pylint: disable=unexpected-keyword-arg

    def _check_one_backbone(self, backbone_cls, backbone_name, test_shape):
        '''
        Base checksfor backbones: can process input and return 4D tensor.
        '''

        if test_shape:
            backbone = backbone_cls(input_channels=1)
            input_batch = self.get_input_batch(True)
        else:
            backbone = backbone_cls()
            input_batch = self.get_input_batch(False)

        outputs = backbone(input_batch)
        self.assertTrue(tf.is_tensor(outputs), f'Output of "{backbone_name}" is not a tensor')
        self.assertEqual(tf.rank(outputs), 4, f'Outputs for "{backbone_name}" must have rank 4')

    def test_resnet50v2(self):
        '''
        Check :func:`backbones.Resnet50V2` model.
        '''

        self._check_one_backbone(backbones.Resnet50V2, 'Resnet50V2', True)

    def test_efficient_net_b4(self):
        '''
        Check :func:`backbones.EfficientNetB4` model.
        '''

        self._check_one_backbone(backbones.EfficientNetB4, 'EfficientNetB4', True)

    @unittest.skipIf(len(GPU_DEVICES) == 0, "Not implemented error in CONV operation at CPU")
    def test_mobile_net_v2(self):
        '''
        Check :func:`backbones.MobileNetV2` model.
        '''

        self._check_one_backbone(backbones.MobileNetV2, 'MobileNetV2', False)

    @unittest.skipIf(len(GPU_DEVICES) == 0, "Not implemented error in CONV operation at CPU")
    def test_dense_net_121(self):
        '''
        Check :func:`backbones.DenseNet121` model.
        '''

        self._check_one_backbone(backbones.DenseNet121, 'DenseNet121', False)
