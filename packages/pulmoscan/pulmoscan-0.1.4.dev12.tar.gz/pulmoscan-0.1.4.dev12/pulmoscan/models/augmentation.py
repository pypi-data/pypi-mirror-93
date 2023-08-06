'''
Contains augmentation utils.
'''

import typing

import gin
import tensorflow as tf

import tensorflow.keras.layers.experimental.preprocessing as preprocessing_layers


@gin.configurable(blacklist=['input_layer'])
def create_base_preprocessing_pipeline(
        input_layer: tf.keras.layers.Layer,
        image_size: typing.Tuple[int, int] = (284, 284),
        maximum_pixel_value: float = 255,
        flip_mode: str = 'horizontal_and_vertical',
        rotation_factor: float = 0.1,
        random_state: int = 543657
    ) -> tf.keras.layers.Layer:
    """Given input layer applies preprocessing transformations.

    Args:
        input_layer (tf.keras.layers.Layer): Keras layer. Means input layer for images.
        image_size (Tuple[int, int], optional): Size of input image as tuple with two elements.
            Defaults to (284, 284). Must be consistent with ``input_layer``.
        maximum_pixel_value (float, optional): Upper bound for pixel values. Defaults to 255.
        flip_mode (str, optional): How to flip input image. Defaults to 'horizontal_and_vertical'.
            See keras documentation for more options:
            https://www.tensorflow.org/api_docs/python/tf/keras/layers/experimental/preprocessing/RandomFlip
        rotation_factor (float, optional): a float representing fraction of 2*pi. Defaults to 0.1. See
            https://www.tensorflow.org/api_docs/python/tf/keras/layers/experimental/preprocessing/RandomRotation
        random_state (int, optional): Random state for transformations. Defaults to 543657.

    Returns:
        tf.keras.layers.Layer: Output of preprocessing pipeline.
    """

    features = preprocessing_layers.Normalization()(input_layer)
    features = preprocessing_layers.Resizing(*image_size)(features)
    features = preprocessing_layers.Rescaling(1. / maximum_pixel_value)(features)
    features = preprocessing_layers.RandomFlip(flip_mode, seed=random_state)(features)
    features = preprocessing_layers.RandomRotation(rotation_factor, seed=random_state)(features)
    return features
