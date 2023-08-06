'''
Module contains custom metrics for :func:`pulmoscan` package.
'''

import tensorflow as tf


class ConfusionMatrix(tf.keras.metrics.Metric):
    """Builds `confusion matrix: <https://en.wikipedia.org/wiki/Confusion_matrix>`_. by
    batches.

    Args:
        n_classes (int): Number of classes to recognize.
        name (str, optional): Name of the layer. Defaults to 'confusion_matrix'.
    """

    def __init__(self, n_classes: int, name: str = 'confusion_matrix'):
        super().__init__(name=name)
        self._conf_matrix = self.add_weight(
            name='conf_matrix', shape=(n_classes, n_classes), initializer='zeros', dtype='int32'
        )
        self._n_classes: int = n_classes

    def reset_states(self):
        self._conf_matrix.assign(tf.zeros((self._n_classes, self._n_classes), dtype='int32'))

    def update_state(self, y_true, y_pred, sample_weight=None): # pylint: disable=arguments-differ
        y_pred_sparse = tf.argmax(y_pred, -1)
        local_matrix = tf.math.confusion_matrix(y_true, y_pred_sparse, weights=sample_weight, num_classes=self._n_classes)
        self._conf_matrix.assign_add(local_matrix)

    def result(self):
        return self._conf_matrix


def precision_from_confusion_matrix(confusion_matrix: tf.Tensor) -> tf.Tensor:
    """
    Calculates precision vector :math:`P` from the confusion matrix.
    :math:`i-th` elements of the resulting vector gives precision for
    class with label :math:`i`.
    """

    true_positives = tf.linalg.diag_part(confusion_matrix)
    denominator = tf.reduce_sum(confusion_matrix, 0)
    return tf.math.divide_no_nan(
        tf.cast(true_positives, 'float32'),
        tf.cast(denominator, 'float32')
    )


class VectorPrecision(ConfusionMatrix):
    """Calculates precision for multiple classes.

    Args:
        n_classes (int): Number of classes to recognize.
        name (str, optional): Name of the metric. Defaults to 'precision'.
    """

    def __init__(self, n_classes: int, name: str = 'precision'):
        super().__init__(n_classes, name=name)

    def result(self):
        confusion_matrix = super().result()
        return precision_from_confusion_matrix(confusion_matrix)


class ClassPrecision(VectorPrecision):
    """Calculates precision for a particular class.

    Args:
        n_classes (int): Number of classes to recognize.
        name (str, optional): Name of the metric. Defaults to 'precision'.
    """

    def __init__(self, n_classes: int, class_to_take: int, name: str = 'precision'):
        super().__init__(n_classes, name=name)
        self._class_to_take = class_to_take

    def result(self):
        return super().result()[self._class_to_take]


def recall_from_confusion_matrix(confusion_matrix: tf.Tensor) -> tf.Tensor:
    """
    Calculates recall vector :math:`R` from the confusion matrix.
    :math:`i-th` elements of the resulting vector gives recall for
    class with label :math:`i`.
    """

    true_positives = tf.linalg.diag_part(confusion_matrix)
    denominator = tf.reduce_sum(confusion_matrix, 1)
    return tf.math.divide_no_nan(
        tf.cast(true_positives, 'float32'),
        tf.cast(denominator, 'float32')
    )

class VectorRecall(ConfusionMatrix):
    """Calculates recall for multiple classes.

    Args:
        n_classes (int): Total number of classes to recognize.
        name (str, optional): Name of the layer. Defaults to 'recall'.
    """

    def __init__(self, n_classes: int, name: str = 'recall'):
        super().__init__(n_classes, name=name)

    def result(self):
        confusion_matrix = super().result()
        return recall_from_confusion_matrix(confusion_matrix)


class ClassRecall(VectorRecall):
    """Calculates recall for a particular class.

    Args:
        n_classes (int): Number of classes to recognize.
        name (str, optional): Name of the metric. Defaults to 'precision'.
    """

    def __init__(self, n_classes: int, class_to_take: int, name: str = 'recall'):
        super().__init__(n_classes, name=name)
        self._class_to_take = class_to_take

    def result(self):
        return super().result()[self._class_to_take]


class VectorF1(ConfusionMatrix):
    """Calculates f1 score for multiple classes.

    Args:
        n_classes (int): Number of classes to recognize.
        name (str, optional): Name of the metric. Defaults to 'micro_f1'.
    """

    def __init__(self, n_classes: int, name: str = 'micro_f1'):
        super().__init__(n_classes, name=name)

    def result(self):
        confusion_matrix = super().result()
        precision = precision_from_confusion_matrix(confusion_matrix)
        recall = recall_from_confusion_matrix(confusion_matrix)
        return 2 * tf.math.divide_no_nan(
            precision * recall, precision + recall
        )


class ClassF1(VectorF1):
    """Calculates precision for a particular class.

    Args:
        n_classes (int): Number of classes to recognize.
        name (str, optional): Name of the metric. Defaults to 'precision'.
    """

    def __init__(self, n_classes: int, class_to_take: int, name: str = 'f1'):
        super().__init__(n_classes, name=name)
        self._class_to_take = class_to_take

    def result(self):
        return super().result()[self._class_to_take]
