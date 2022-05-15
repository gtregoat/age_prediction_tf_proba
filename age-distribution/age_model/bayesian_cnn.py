"""
https://github.com/tensorflow/probability/issues/1350
"""
import tensorflow as tf
import tensorflow_probability as tfp
from tensorflow.keras.models import Sequential
from typing import Any
from .losses import nll, negloglik
from .bayesian_layers import conv_reparameterization_layer, dense_reparametrization_layer


class TfProbabilityCnnClassifier(Sequential):
    def __init__(self, input_dim: tuple, n_classes: int, optimizer: Any = None, metrics: list = None, loss: Any = None):
        super().__init__()
        if optimizer is None:
            optimizer = tf.keras.optimizers.Adam(0.001)
        if metrics is None:
            metrics = ['accuracy']
        if loss is None:
            loss = nll

        self.add(tf.keras.layers.InputLayer(input_dim))

        self.add(conv_reparameterization_layer(16, 3, 'swish'))
        self.add(tf.keras.layers.MaxPooling2D(2))

        self.add(conv_reparameterization_layer(32, 3, 'swish'))
        self.add(tf.keras.layers.MaxPooling2D(2))

        self.add(conv_reparameterization_layer(64, 3, 'swish'))
        self.add(tf.keras.layers.MaxPooling2D(2))

        self.add(conv_reparameterization_layer(128, 3, 'swish'))
        self.add(tf.keras.layers.GlobalMaxPooling2D())

        self.add(dense_reparametrization_layer(n_classes))
        self.add(tfp.layers.OneHotCategorical(n_classes))

        self.compile(loss=loss,
                     optimizer=optimizer,
                     metrics=metrics)


class TfProbabilityCnnRegressor(Sequential):
    def __init__(self, input_dim: tuple, optimizer: Any = None, metrics: list = None, loss: Any = None,
                 scale: float = 10):
        super().__init__()
        if optimizer is None:
            optimizer = tf.keras.optimizers.Adam(0.01)
        if metrics is None:
            metrics = ['mean_squared_error']
        if loss is None:
            loss = negloglik

        self.add(tf.keras.layers.InputLayer(input_dim))

        self.add(conv_reparameterization_layer(16, 3, 'swish'))
        self.add(tf.keras.layers.MaxPooling2D(2))

        self.add(conv_reparameterization_layer(32, 3, 'swish'))
        self.add(tf.keras.layers.MaxPooling2D(2))

        self.add(conv_reparameterization_layer(64, 3, 'swish'))
        self.add(tf.keras.layers.MaxPooling2D(2))

        self.add(conv_reparameterization_layer(128, 3, 'swish'))
        self.add(tf.keras.layers.GlobalMaxPooling2D())

        self.add(dense_reparametrization_layer(1))
        self.add(tfp.layers.DistributionLambda(lambda t: tfp.distributions.Normal(loc=t, scale=scale)))

        self.compile(loss=loss,
                     optimizer=optimizer,
                     metrics=metrics)
