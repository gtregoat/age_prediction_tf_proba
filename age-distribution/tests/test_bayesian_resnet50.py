"""
Test if the resnet50 can be created.
"""
import pytest
import numpy as np
from age_model import bayesian_resnet50
from tensorflow.keras import backend as K


@pytest.fixture(autouse=True)
def reset_keras_layer_count():
    yield
    K.clear_session()


def test_init_regressor():
    model = bayesian_resnet50.TfProbabilityResnet50Classifier(input_dim=(10, 10, 1),
                                                              n_classes=2)
    assert model.built


# def test_init_classifier():
#     model = bayesian_resnet50.TfProbabilityResnet50Classifier(input_dim=(10, 10, 1), n_classes=2)
#     assert model.built


#
# def test_fit_regressor():
#     model = bayesian_resnet50.TfProbabilityResnet50Regressor(input_dim=(10, 10, 1))
#     x = np.ones([5, 10, 10])
#     y = np.ones([5])
#     model.fit(x, y)
#     assert "loss" in model.history.history and "mean_squared_error" in model.history.history
#
#
# def test_fit_classifier():
#     model = bayesian_resnet50.TfProbabilityResnet50Classifier(input_dim=(10, 10, 1), n_classes=2)
#     x = np.ones([5, 10, 10])
#     y = np.column_stack([np.ones([5]), np.zeros([5])])
#     model.fit(x, y)
#     assert "loss" in model.history.history and "accuracy" in model.history.history
