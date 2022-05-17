"""
Reference: Bayesian Layers: A module for Neural Network Uncertainty
"""
import tensorflow as tf
import tensorflow_probability as tfp
from typing import Any
from .losses import negloglik
from .bayesian_layers import conv_reparameterization_layer, dense_reparametrization_layer


def conv_block(inputs, kernel_size, filters: list, strides=(2, 2)):
    filters1, filters2, filters3 = filters
    x = conv_reparameterization_layer(filters=filters1,
                                      kernel_size=(1, 1),
                                      activation=None,
                                      strides=strides
                                      )(inputs)
    x = tf.keras.layers.BatchNormalization(axis=3)(x)
    x = tf.keras.layers.Activation("relu")(x)
    x = conv_reparameterization_layer(filters=filters2,
                                      kernel_size=kernel_size,
                                      activation=None,
                                      )(x)
    x = tf.keras.layers.BatchNormalization(axis=3)(x)
    x = tf.keras.layers.Activation("relu")(x)
    x = conv_reparameterization_layer(filters=filters3,
                                      kernel_size=(1, 1),
                                      activation=None,
                                      )(x)
    x = tf.keras.layers.BatchNormalization(axis=3)(x)
    shortcut = conv_reparameterization_layer(filters=filters3,
                                             kernel_size=(1, 1),
                                             activation=None,
                                             strides=strides
                                             )(inputs)
    shortcut = tf.keras.layers.BatchNormalization(axis=3)(shortcut)
    x = tf.keras.layers.add([x, shortcut])
    x = tf.keras.layers.Activation("relu")(x)
    return x


def identity_block(inputs, kernel_size, filters):
    filters1, filters2, filters3 = filters
    x = conv_reparameterization_layer(filters=filters1,
                                      kernel_size=(1, 1),
                                      activation=None,
                                      )(inputs)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)
    x = conv_reparameterization_layer(filters=filters2, kernel_size=kernel_size,
                                      activation=None)(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.Activation("relu")(x)
    x = conv_reparameterization_layer(filters=filters3,
                                      kernel_size=(1, 1),
                                      activation=None,
                                      )(x)
    x = tf.keras.layers.BatchNormalization()(x)
    x = tf.keras.layers.add([x, inputs])
    x = tf.keras.layers.Activation("relu")(x)
    return x


class TfProbabilityResnet50Classifier(tf.keras.models.Model):
    def __init__(self, input_dim: tuple, n_classes: int, optimizer: Any = None, metrics: list = None, loss: Any = None):
        if optimizer is None:
            optimizer = tf.keras.optimizers.Adam()
        if metrics is None:
            metrics = ['accuracy']
        if loss is None:
            loss = "categorical_crossentropy"

        inputs = tf.keras.layers.Input(shape=input_dim,
                                       dtype="float32")
        x = tf.keras.layers.ZeroPadding2D((3, 3))(inputs)
        x = conv_reparameterization_layer(filters=64,
                                          kernel_size=(7, 7),
                                          activation=None,
                                          strides=(2, 2),
                                          padding="valid"
                                          )(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)
        x = tf.keras.layers.ZeroPadding2D((1, 1))(x)
        x = tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2))(x)

        x = conv_block(x, 3, [64, 64, 256], strides=(1, 1))
        x = identity_block(x, 3, [64, 64, 256])
        x = identity_block(x, 3, [64, 64, 256])

        x = conv_block(x, 3, [128, 128, 512])
        x = identity_block(x, 3, [128, 128, 512])
        x = identity_block(x, 3, [128, 128, 512])
        x = identity_block(x, 3, [128, 128, 512])

        x = conv_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])

        x = conv_block(x, 3, [512, 512, 2048])
        x = identity_block(x, 3, [512, 512, 2048])
        x = identity_block(x, 3, [512, 512, 2048])

        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = dense_reparametrization_layer(n_classes)(x)
        super().__init__(inputs, x, name="bayesian_resnet_50")
        self.compile(loss=loss,
                     optimizer=optimizer,
                     metrics=metrics)


class TfProbabilityResnet50Regressor(tf.keras.models.Model):
    def __init__(self, input_dim: tuple, optimizer: Any = None, metrics: list = None, loss: Any = None,
                 scale=1):
        if optimizer is None:
            optimizer = tf.keras.optimizers.Adam()
        if metrics is None:
            metrics = ['mean_squared_error']
        if loss is None:
            loss = negloglik

        inputs = tf.keras.layers.Input(shape=input_dim,
                                       dtype="float32")
        x = tf.keras.layers.ZeroPadding2D((3, 3))(inputs)
        x = conv_reparameterization_layer(filters=64,
                                          kernel_size=(7, 7),
                                          activation=None,
                                          strides=(2, 2),
                                          padding="valid"
                                          )(x)
        x = tf.keras.layers.BatchNormalization()(x)
        x = tf.keras.layers.Activation("relu")(x)
        x = tf.keras.layers.ZeroPadding2D((1, 1))(x)
        x = tf.keras.layers.MaxPooling2D((3, 3), strides=(2, 2))(x)
        x = conv_block(x, 3, [64, 64, 256], strides=(1, 1))
        x = identity_block(x, 3, [64, 64, 256])
        x = identity_block(x, 3, [64, 64, 256])
        x = conv_block(x, 3, [128, 128, 512])
        x = identity_block(x, 3, [128, 128, 512])
        x = identity_block(x, 3, [128, 128, 512])
        x = identity_block(x, 3, [128, 128, 512])
        x = conv_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = identity_block(x, 3, [256, 256, 1024])
        x = conv_block(x, 3, [512, 512, 2048])
        x = identity_block(x, 3, [512, 512, 2048])
        x = identity_block(x, 3, [512, 512, 2048])
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tfp.layers.DistributionLambda(lambda t: tfp.distributions.Normal(loc=t, scale=scale))(x)
        super().__init__(inputs, x, name="bayesian_resnet_50")
        self.compile(loss=loss,
                     optimizer=optimizer,
                     metrics=metrics)
