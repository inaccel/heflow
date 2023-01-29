import joblib
import numpy
import os
import tenseal


class CKKSTensor:
    context = tenseal.context_from(
        joblib.load(os.getenv('HEFLOW_CKKS', 'id_ckks')))

    def __getstate__(self):
        return {'data': self.backend.serialize()}

    def __init__(self, data):
        self.backend = tenseal.ckks_tensor(self.context, data)

    def __setstate__(self, state):
        self.backend = tenseal.ckks_tensor_from(self.context, state['data'])

    def add(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        return CKKSTensor(self.backend.add(other))

    def add_(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        self.backend.add_(other)
        return self

    def broadcast_to(self, shape):
        return CKKSTensor(self.backend.broadcast(shape))

    def broadcast_to_(self, shape):
        self.backend.broadcast_(shape)
        return self

    def clone(self):
        return CKKSTensor(self.backend.copy())

    def dot(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        return CKKSTensor(self.backend.dot(other))

    def dot_(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        self.backend.dot_(other)
        return self

    @property
    def dtype(self):
        return 'float64'

    def mm(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        return CKKSTensor(self.backend.mm(other))

    def mm_(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        self.backend.mm_(other)
        return self

    def mul(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        return CKKSTensor(self.backend.mul(other))

    def mul_(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        self.backend.mul_(other)
        return self

    def neg(self):
        return CKKSTensor(self.backend.neg())

    def neg_(self):
        self.backend.neg_()
        return self

    def numpy(self):
        backend = self.backend.decrypt()
        return numpy.asarray(backend.raw, backend.dtype).reshape(backend.shape)

    def polyval(self, coeffs):
        return CKKSTensor(self.backend.polyval(coeffs))

    def polyval_(self, coeffs):
        self.backend.polyval_(coeffs)
        return self

    def pow(self, exponent):
        return CKKSTensor(self.backend.pow(exponent))

    def pow_(self, exponent):
        self.backend.pow_(exponent)
        return self

    def reshape(self, shape):
        return CKKSTensor(self.backend.reshape(shape))

    def reshape_(self, shape):
        self.backend.reshape_(shape)
        return self

    @property
    def shape(self):
        return self.backend.shape

    def square(self):
        return CKKSTensor(self.backend.square())

    def square_(self):
        self.backend.square_()
        return self

    def sub(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        return CKKSTensor(self.backend.sub(other))

    def sub_(self, other):
        if isinstance(other, CKKSTensor):
            other = other.backend

        self.backend.sub_(other)
        return self

    def sum(self):
        return CKKSTensor(self.backend.sum())

    def sum_(self):
        self.backend.sum_()
        return self

    def transpose(self):
        return CKKSTensor(self.backend.transpose())

    def transpose_(self):
        self.backend.transpose_()
        return self


def ckks_tensor(data):
    return CKKSTensor(data)
