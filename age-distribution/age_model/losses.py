"""
Constains custom losses for the bayesian deep neural networks
"""


def nll(y_true, y_pred):
    return -y_pred.log_prob(y_true)


def negloglik(y, rv_y):
    return -rv_y.log_prob(y)
