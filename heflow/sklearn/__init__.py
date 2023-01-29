import heflow
import heflow.sklearn.linear_model
import sklearn.linear_model


def log_model(model):
    if isinstance(model, sklearn.linear_model.LogisticRegression):
        return heflow.log_model(
            heflow.sklearn.linear_model.LogisticRegression(model))

    raise TypeError(f'invalid model instance: {type(model)}')


def save_model(path, model):
    if isinstance(model, sklearn.linear_model.LogisticRegression):
        return heflow.save_model(
            path, heflow.sklearn.linear_model.LogisticRegression(model))

    raise TypeError(f'invalid model instance: {type(model)}')
