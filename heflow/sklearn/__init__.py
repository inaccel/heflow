import heflow
import heflow.sklearn.linear_model
import sklearn.linear_model


def log_model(model,
              *,
              registered_model_name=None,
              await_registration_for=300):
    if isinstance(model, sklearn.linear_model.LogisticRegression):
        return heflow.log_model(
            heflow.sklearn.linear_model.LogisticRegression(model),
            registered_model_name=registered_model_name,
            await_registration_for=await_registration_for)
    else:
        raise TypeError(f'invalid model instance: {type(model)}')


def save_model(path, model):
    if isinstance(model, sklearn.linear_model.LogisticRegression):
        heflow.save_model(
            path, heflow.sklearn.linear_model.LogisticRegression(model))
    else:
        raise TypeError(f'invalid model instance: {type(model)}')
