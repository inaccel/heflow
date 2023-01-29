import heflow.tensors
import mlserver.codecs
import mlserver.codecs.utils
import mlserver.types
import pickle
import typing


@mlserver.codecs.register_input_codec
class CKKSTensorCodec(mlserver.codecs.InputCodec):
    ContentType: typing.ClassVar[str] = 'heflow/ckks_tensor'
    TypeHint: typing.ClassVar[typing.Type] = heflow.tensors.CKKSTensor

    @classmethod
    def can_encode(cls, payload: typing.Any) -> bool:
        return isinstance(payload, heflow.tensors.CKKSTensor)

    @classmethod
    def encode_output(cls, name: str, payload: heflow.tensors.CKKSTensor,
                      **kwargs) -> mlserver.types.ResponseOutput:
        return mlserver.types.ResponseOutput(
            name=name,
            shape=payload.shape,
            datatype='BYTES',
            parameters=mlserver.types.Parameters(content_type=cls.ContentType),
            data=[pickle.dumps(payload)],
        )

    @classmethod
    def decode_output(
        cls, response_output: mlserver.types.ResponseOutput
    ) -> heflow.tensors.CKKSTensor:
        return pickle.loads(response_output.data[0])

    @classmethod
    def encode_input(cls, name: str, payload: heflow.tensors.CKKSTensor,
                     **kwargs) -> mlserver.types.RequestInput:
        return mlserver.types.RequestInput(
            name=name,
            shape=payload.shape,
            datatype='BYTES',
            parameters=mlserver.types.Parameters(content_type=cls.ContentType),
            data=[pickle.dumps(payload)],
        )

    @classmethod
    def decode_input(
        cls, request_input: mlserver.types.RequestInput
    ) -> heflow.tensors.CKKSTensor:
        return pickle.loads(request_input.data[0])


class InputRequestCodec(mlserver.codecs.RequestCodec):
    InputCodec: typing.Optional[mlserver.codecs.InputCodecLike] = None

    @classmethod
    def can_encode(cls, payload: typing.Any) -> bool:
        if cls.InputCodec is None:
            return False

        if isinstance(payload, tuple):
            payloads = payload
        else:
            payloads = (payload, )
        for payload in payloads:
            if not cls.InputCodec.can_encode(payload):
                return False
        return True

    @classmethod
    def encode_response(
        cls,
        model_name: str,
        payload: typing.Any,
        model_version: typing.Optional[str] = None,
        **kwargs,
    ) -> mlserver.types.InferenceResponse:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f'No input codec found for {type(cls)} request codec')

        outputs = []
        if isinstance(payload, tuple):
            payloads = payload
        else:
            payloads = (payload, )
        for index, payload in enumerate(payloads, 1):
            outputs.append(
                cls.InputCodec.encode_output(
                    f'{mlserver.codecs.utils.DefaultOutputPrefix}{index}',
                    payload, **kwargs))
        return mlserver.types.InferenceResponse(
            model_name=model_name,
            model_version=model_version,
            parameters=mlserver.types.Parameters(content_type=cls.ContentType),
            outputs=outputs)

    @classmethod
    def decode_response(
            cls, response: mlserver.types.InferenceResponse) -> typing.Any:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f'No input codec found for {type(cls)} request codec')

        payloads = ()
        for output in response.outputs:
            payloads += (cls.InputCodec.decode_output(output), )
        if len(payloads) == 1:
            return payloads[0]
        return payloads

    @classmethod
    def encode_request(cls, payload: typing.Any,
                       **kwargs) -> mlserver.types.InferenceRequest:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f'No input codec found for {type(cls)} request codec')

        if isinstance(payload, tuple):
            payloads = payload
        else:
            payloads = (payload, )
        inputs = []
        for index, payload in enumerate(payloads, 1):
            inputs.append(
                cls.InputCodec.encode_input(
                    f'{mlserver.codecs.utils.DefaultInputPrefix}{index}',
                    payload, **kwargs))
        return mlserver.types.InferenceRequest(
            parameters=mlserver.types.Parameters(content_type=cls.ContentType),
            inputs=inputs)

    @classmethod
    def decode_request(cls,
                       request: mlserver.types.InferenceRequest) -> typing.Any:
        if cls.InputCodec is None:
            raise NotImplementedError(
                f'No input codec found for {type(cls)} request codec')

        payloads = ()
        for input in request.inputs:
            payloads += (cls.InputCodec.decode_input(input), )
        if len(payloads) == 1:
            return payloads[0]
        return payloads


@mlserver.codecs.register_request_codec
class CKKSTensorRequestCodec(InputRequestCodec):
    InputCodec: typing.Optional[
        mlserver.codecs.InputCodecLike] = CKKSTensorCodec
    ContentType: typing.ClassVar[str] = InputCodec.ContentType
    TypeHint: typing.ClassVar[typing.Type] = InputCodec.TypeHint
