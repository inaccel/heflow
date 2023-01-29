import mlflow.pyfunc


def load_model(model_uri: str):
    return mlflow.pyfunc.load_model(model_uri).unwrap_python_model()


def log_model(model):
    return mlflow.pyfunc.log_model('model', python_model=model)


def save_model(path, model):
    return mlflow.pyfunc.save_model(path, python_model=model)
