import mlflow.pyfunc


def load_model(model_uri: str):
    return mlflow.pyfunc.load_model(model_uri).unwrap_python_model().unwrap()


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

    return mlflow.pyfunc.save_model(path, python_model=PythonModel(model))
