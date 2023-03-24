import functools
import heflow.codecs
import inspect
import mlflow
import mlserver


@functools.singledispatch
def ckks_model(function):

    @functools.wraps(function)
    def stub(*args, **kwargs):
        if not hasattr(stub, 'channel'):
            return function(*args, **kwargs)

        signature = inspect.signature(function).bind(*args, **kwargs)
        signature.apply_defaults()

        return heflow.codecs.CKKSTensorRequestCodec.decode_response(
            mlserver.grpc.converters.ModelInferResponseConverter.to_types(
                mlserver.grpc.dataplane_pb2_grpc.GRPCInferenceServiceStub(
                    stub.channel).ModelInfer(
                        mlserver.grpc.converters.ModelInferRequestConverter.
                        from_types(heflow.codecs.CKKSTensorRequestCodec.
                                   encode_request(signature.args),
                                   model_name='mlflow-model'))))

    def connect(channel):
        setattr(stub, 'channel', channel)
        return stub

    setattr(stub, 'connect', connect)

    def disconnect():
        if hasattr(stub, 'channel'):
            delattr(stub, 'channel')
        return stub

    setattr(stub, 'disconnect', disconnect)

    setattr(stub, '__infer__', function)

    return stub


@ckks_model.register
def _(infer: str):

    def decorate(cls):
        setattr(cls, '__infer__', getattr(cls, infer))

        def connect(self, channel):
            setattr(self, 'channel', channel)
            return self

        assert not hasattr(cls, 'connect')
        setattr(cls, 'connect', connect)

        def disconnect(self):
            if hasattr(self, 'channel'):
                delattr(self, 'channel')
            return self

        assert not hasattr(cls, 'disconnect')
        setattr(cls, 'disconnect', disconnect)

        @functools.wraps(cls.__infer__)
        def stub(self, *args, **kwargs):
            if not hasattr(self, 'channel'):
                return self.__infer__(*args, **kwargs)

            signature = inspect.signature(self.__infer__).bind(*args, **kwargs)
            signature.apply_defaults()

            return heflow.codecs.CKKSTensorRequestCodec.decode_response(
                mlserver.grpc.converters.ModelInferResponseConverter.to_types(
                    mlserver.grpc.dataplane_pb2_grpc.GRPCInferenceServiceStub(
                        self.channel).ModelInfer(
                            mlserver.grpc.converters.
                            ModelInferRequestConverter.from_types(
                                heflow.codecs.CKKSTensorRequestCodec.
                                encode_request(signature.args),
                                model_name='mlflow-model'))))

        setattr(cls, infer, stub)

        return cls

    return decorate


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

    mlflow.pyfunc.save_model(path, python_model=PythonModel(model))
