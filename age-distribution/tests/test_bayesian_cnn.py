"""
Test if the resnet50 can be created.
"""
import pytest
import numpy as np
from age_model import bayesian_cnn
from tensorflow.keras import backend as K


@pytest.fixture(autouse=True)
def reset_keras_layer_count():
    yield
    K.clear_session()


def test_init_regressor():
    model = bayesian_cnn.TfProbabilityCnnRegressor(input_dim=(10, 10, 1))
    assert model.built
    expected_network_layers = ['conv2d_reparameterization',
                               'max_pooling2d',
                               'conv2d_reparameterization_1',
                               'max_pooling2d_1',
                               'conv2d_reparameterization_2',
                               'max_pooling2d_2',
                               'conv2d_reparameterization_3',
                               'global_max_pooling2d',
                               'dense_reparameterization',
                               'distribution_lambda']
    assert [i.name for i in model.layers] == expected_network_layers


def test_init_classifier():
    model = bayesian_cnn.TfProbabilityCnnClassifier(input_dim=(10, 10, 1), n_classes=2)
    assert model.built
    expected_network_layers = ['conv2d_reparameterization',
                               'max_pooling2d',
                               'conv2d_reparameterization_1',
                               'max_pooling2d_1',
                               'conv2d_reparameterization_2',
                               'max_pooling2d_2',
                               'conv2d_reparameterization_3',
                               'global_max_pooling2d',
                               'dense_reparameterization',
                               'one_hot_categorical']
    assert [i.name for i in model.layers] == expected_network_layers


def test_fit_regressor():
    model = bayesian_cnn.TfProbabilityCnnRegressor(input_dim=(10, 10, 1))
    x = np.ones([5, 10, 10])
    y = np.ones([5])
    model.fit(x, y)
    assert "loss" in model.history.history and "mean_squared_error" in model.history.history


def test_fit_classifier():
    model = bayesian_cnn.TfProbabilityCnnClassifier(input_dim=(10, 10, 1), n_classes=2)
    x = np.ones([5, 10, 10])
    y = np.column_stack([np.ones([5]), np.zeros([5])])
    model.fit(x, y)
    assert "loss" in model.history.history and "accuracy" in model.history.history
