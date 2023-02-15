import heflow.models
import math


@heflow.models.ckks_model
def he_exponential(he_x):
    return he_x.polyval_([1, 1, 1 / 2, 1 / 6, 1 / 24, 1 / 120])


@heflow.models.ckks_model
def he_sigmoid(he_x):
    return he_x.polyval_([1 / 2, 1 / 4, 0, -1 / 48, 0, 1 / 480])


@heflow.models.ckks_model
def he_softplus(he_x):
    return he_x.polyval_([math.log(2), 1 / 2, 1 / 8, 0, -1 / 192, 0, 1 / 2880])


@heflow.models.ckks_model
def he_swish(he_x):
    return he_x.polyval_([0, 1 / 2, 1 / 4, 0, -1 / 48, 0, 1 / 480])
