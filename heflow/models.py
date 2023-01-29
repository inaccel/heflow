import heflow.codecs
import mlflow.pyfunc
import mlflow.pyfunc.mlserver
import mlserver.grpc.converters
import mlserver.grpc.dataplane_pb2_grpc


def ckks_model(infer: str):

    def decorate(cls):
        setattr(cls, '__call__', getattr(cls, infer))

        def connect(self, channel):
            setattr(self, 'channel', channel)
            return self

        setattr(cls, 'connect', connect)

        def disconnect(self):
            if hasattr(self, 'channel'):
                delattr(self, 'channel')
            return self

        setattr(cls, 'disconnect', disconnect)

        def stub(self, *args):
            if not hasattr(self, 'channel'):
                return self(*args)

            return heflow.codecs.CKKSTensorRequestCodec.decode_response(
                mlserver.grpc.converters.ModelInferResponseConverter.to_types(
                    mlserver.grpc.dataplane_pb2_grpc.GRPCInferenceServiceStub(
                        self.channel).ModelInfer(
                            mlserver.grpc.converters.
                            ModelInferRequestConverter.from_types(
                                heflow.codecs.CKKSTensorRequestCodec.
                                encode_request(args),
                                model_name=mlflow.pyfunc.mlserver.
                                MLServerDefaultModelName))))

        setattr(cls, infer, stub)

        def predict(self, context, model_input):
            if isinstance(model_input, tuple):
                return self(*model_input)
            else:
                return self(model_input)

        return type('CKKSModel', (cls, mlflow.pyfunc.PythonModel),
                    {'predict': predict})

    return decorate
