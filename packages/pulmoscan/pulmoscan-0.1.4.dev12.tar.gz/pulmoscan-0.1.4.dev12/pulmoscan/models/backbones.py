'''
Contains image encoders.
'''

import gin
import tensorflow as tf


# Violating name conventions to unify interfaces with another
# image incoders:
@gin.configurable
def AlexNet() -> tf.keras.Model: # pylint: disable=invalid-name
    '''
    Creates AlexNet encoder for images.
    '''

    model = tf.keras.models.Sequential([
        tf.keras.layers.Conv2D(filters=96, kernel_size=(11,11), strides=(4,4), activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
        tf.keras.layers.Conv2D(filters=256, kernel_size=(5,5), strides=(1,1), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
        tf.keras.layers.Conv2D(filters=384, kernel_size=(3,3), strides=(1,1), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(filters=384, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Conv2D(filters=256, kernel_size=(1,1), strides=(1,1), activation='relu', padding="same"),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.MaxPool2D(pool_size=(3,3), strides=(2,2)),
    ])
    return model


def grayscale_batch_to_rgb(batch: tf.Tensor) -> tf.Tensor:
    """Converts grayscale image to RGB format using
    duplication of pixel values three times across
    the last dimension.

    Args:
        batch (tf.Tensor): Batch of input images. Must have
        shape ``[b, h, w, 1]``.

    Returns:
        tf.Tensor: Tensor of shape ``[b, h, w,  3]``.
    """

    return tf.repeat(batch, 3, -1)

@gin.configurable
class Resnet50V2(tf.keras.layers.Layer):
    '''
    Wrapper around :func:`tf.keras.applications.ResNet50V2` that
    simplifies its creation.

    Expects float image with shape ``[batch, h, w, c]`` as input. Pixel
    must be in range ``[0, 255]``.

    Args:
        input_channels (int): Number of channels in input image. If there is
            one channel (image is grayscaled), it will be processed
            dirrefently.
    '''

    def __init__(self, input_channels: int = 1, name: str = 'resnet_50'):
        super().__init__(name=name)

        self._input_channels = input_channels
        self._keras_model = tf.keras.applications.ResNet50V2(
            include_top=False, weights='imagenet', pooling=None
        )

    def preprocess_inputs(self, inputs: tf.Tensor) -> tf.Tensor: # pylint: disable=no-self-use
        '''
        Call image preprocessing function.
        '''
        if self._input_channels == 1:
            inputs = grayscale_batch_to_rgb(inputs)

        return tf.keras.applications.resnet_v2.preprocess_input(inputs)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor: # pylint: disable=arguments-differ
        return self._keras_model(self.preprocess_inputs(inputs), training=training)


@gin.configurable
class EfficientNetB4(tf.keras.layers.Layer):
    '''
    Wrapper around :func:`tf.keras.applications.EfficientNetB4` that
    simplifies its creation.

    Expects float image with shape ``[batch, h, w, c]`` as input. Pixel
    must be in range ``[0, 255]``.

    Args:
        input_channels (int): Number of channels in input image. If there is
            one channel (image is grayscaled), it will be processed
            dirrefently.
    '''

    def __init__(self, input_channels: int = 1, name: str = 'efficient_net_b4'):
        super().__init__(name=name)

        self._input_channels: int = input_channels
        self._keras_model = tf.keras.applications.EfficientNetB4(
            include_top=False, weights='imagenet', pooling=None
        )

    def preprocess_inputs(self, inputs: tf.Tensor) -> tf.Tensor: # pylint: disable=no-self-use
        '''
        Call image preprocessing function.
        '''

        if self._input_channels == 1:
            inputs = grayscale_batch_to_rgb(inputs)

        return tf.identity(inputs)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor: # pylint: disable=arguments-differ
        return self._keras_model(self.preprocess_inputs(inputs), training=training)


@gin.configurable
class MobileNetV2(tf.keras.layers.Layer):
    '''
    Wrapper around :func:`tf.keras.applications.MobileNetV2` that
    simplifies its creation.

    Expects float image with shape ``[batch, h, w, c]`` as input. Pixel
    must be in range ``[0, 255]``.

    Args:
        alpha (float): See documentation of :func:`tf.keras.applications.MobileNetV2`
            fordetailed information on that parameter.
        input_channels (int): Number of channels in input image. If there is
            one channel (image is grayscaled), it will be processed
            dirrefently.
    '''

    def __init__(self, name: str = 'mobile_net_v2', input_channels: int = 1, alpha: float = 1.):
        super().__init__(name=name)
        self._input_channels: int = input_channels
        self._keras_model = tf.keras.applications.MobileNetV2(
            include_top=False, weights='imagenet', pooling=None,
            alpha=alpha
        )

    def preprocess_inputs(self, inputs: tf.Tensor) -> tf.Tensor: # pylint: disable=no-self-use
        '''
        Call image preprocessing function.
        '''

        if self._input_channels == 1:
            inputs = grayscale_batch_to_rgb(inputs)

        return tf.keras.applications.mobilenet_v2.preprocess_input(inputs)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor: # pylint: disable=arguments-differ
        return self._keras_model(self.preprocess_inputs(inputs), training=training)


@gin.configurable
class DenseNet121(tf.keras.layers.Layer):
    '''
    Wrapper around :func:`tf.keras.applications.DenseNet121` that
    simplifies its creation.

    Expects float image with shape ``[batch, h, w, c]`` as input. Pixel
    must be in range ``[0, 255]``.

    Args:
        input_channels (int): Number of channels in input image. If there is
            one channel (image is grayscaled), it will be processed
            dirrefently.
    '''

    def __init__(self, name: str = 'densenet121', input_channels: int = 1):
        super().__init__(name=name)
        self._input_channels: int = input_channels
        self._keras_model = tf.keras.applications.DenseNet121(
            include_top=False, weights='imagenet', pooling=None
        )

    def preprocess_inputs(self, inputs: tf.Tensor) -> tf.Tensor: # pylint: disable=no-self-use
        '''
        Call image preprocessing function.
        '''

        if self._input_channels == 1:
            inputs = grayscale_batch_to_rgb(inputs)

        return tf.keras.applications.densenet.preprocess_input(inputs)

    def call(self, inputs: tf.Tensor, training: bool = False) -> tf.Tensor: # pylint: disable=arguments-differ
        return self._keras_model(self.preprocess_inputs(inputs), training=training)
