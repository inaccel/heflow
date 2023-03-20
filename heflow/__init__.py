import functools
import heflow.keys
import joblib
import mlflow
import tempfile


@functools.singledispatch
def load_key(path):
    return joblib.load(path)


@load_key.register
def _(key_uri: str):
    with tempfile.TemporaryDirectory() as tmp:
        return joblib.load(
            mlflow.artifacts.download_artifacts(key_uri, dst_path=tmp))


def load_model(model_uri: str):
    return mlflow.pyfunc.load_model(model_uri).unwrap_python_model().unwrap()


def log_key(key):
    with tempfile.TemporaryDirectory() as tmp:
        if isinstance(key, heflow.keys.CKKSKey):
            path = f'{tmp}/id_ckks.pub'
        else:
            raise mlflow.MlflowException(
                f'`key` must be a subclass of `CKKSKey`. Instead, found an object of type: {type(key)}',
                mlflow.exceptions.INVALID_PARAMETER_VALUE)
        save_key(path, key.public_key())
        heflow.keys.KeysRepository(f'keys:/{key.fingerprint()}').log_artifact(
            path)


def log_model(model,
              *,
              registered_model_name=None,
              await_registration_for=300):

    class PythonModel(mlflow.pyfunc.PythonModel):

        def __init__(self, model):
            self.model = model

        def predict(self, context, model_input):
            if isinstance(model_input, tuple):
                return self.model.__infer__(*model_input)
            else:
                return self.model.__infer__(model_input)

        def unwrap(self):
            return self.model

    return mlflow.pyfunc.log_model(
        'model',
        python_model=PythonModel(model),
        registered_model_name=registered_model_name,
        await_registration_for=await_registration_for)


def save_key(path, key):
    joblib.dump(key, path)


def save_model(path, model):

    class PythonModel(mlflow.pyfunc.PythonModel):

        def __init__(self, model):
            self.model = model

        def predict(self, context, model_input):
            if isinstance(model_input, tuple):
                return self.model.__infer__(*model_input)
            else:
                return self.model.__infer__(model_input)

        def unwrap(self):
            return self.model

    mlflow.pyfunc.save_model(path, python_model=PythonModel(model))
