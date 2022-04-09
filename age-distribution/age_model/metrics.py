"""
Custom metrics to evaluate our models
"""
from tensorflow import math
from tensorflow.keras.losses import mean_absolute_error
import tensorflow as tf
tf.config.experimental_run_functions_eagerly(True)


def mae_for_classification(y_true, y_pred):
    y_true = math.argmax(y_true, 1)
    y_pred = math.argmax(y_pred, 1)
    return mean_absolute_error(y_true, y_pred)


def format_labels(y, buckets: list = None):
    if buckets is None:
        buckets = [
            [i for i in range(13)],
            [i for i in range(13, 18)],
            [i for i in range(18, 24)],
            [i for i in range(25, 34)],
            [i for i in range(35, 44)],
            [i for i in range(45, 64)],
            [i for i in range(64, 101)],
        ]
    # Make segment ids
    segments = tf.concat([tf.tile([i], [len(lst)]) for i, lst in enumerate(buckets)], axis=0)
    # Select columns
    data_cols = tf.gather(tf.transpose(y), tf.concat(buckets, axis=0))
    col_sum = tf.transpose(math.segment_sum(data_cols, segments))
    return math.argmax(col_sum, 1)


def bucketted_accuracy(y_true, y_pred, buckets: list = None):
    y_true = format_labels(y_true, buckets)
    y_pred = format_labels(y_pred, buckets)
    eq = tf.cast(math.equal(y_true, y_pred),  tf.int32)
    return math.reduce_sum(eq) / eq.shape
