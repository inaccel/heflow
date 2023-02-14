import functools
import heflow.codecs
import inspect
import mlflow.pyfunc
import mlflow.pyfunc.mlserver
import mlserver.grpc.converters
import mlserver.grpc.dataplane_pb2_grpc


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
                                   model_name=mlflow.pyfunc.mlserver.
                                   MLServerDefaultModelName))))

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
                                model_name=mlflow.pyfunc.mlserver.
                                MLServerDefaultModelName))))

        setattr(cls, infer, stub)

        return cls

    return decorate
