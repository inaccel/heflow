import base64
import functools
import hashlib
import tenseal


class CKKSKey:

    def __getstate__(self):
        return {'data': self.backend.serialize(save_secret_key=True)}

    @functools.singledispatchmethod
    def __init__(self, coeff_modulus_bit_sizes, poly_modulus_degree,
                 scale_bit_size):
        self.backend = tenseal.context(
            tenseal.SCHEME_TYPE.CKKS,
            poly_modulus_degree,
            coeff_mod_bit_sizes=coeff_modulus_bit_sizes)
        self.backend.global_scale = 2**scale_bit_size
        self.backend.generate_galois_keys()

    @__init__.register
    def _(self, backend: tenseal.Context):
        self.backend = backend

    def __setstate__(self, state):
        self.backend = tenseal.context_from(state['data'])

    @functools.lru_cache
    def fingerprint(self, hash='sha256'):
        if hash == 'md5':
            hexdigest = hashlib.md5(
                self.backend.serialize(save_galois_keys=False,
                                       save_relin_keys=False)).hexdigest()
            return 'MD5:' + ':'.join([
                hexdigest[hex:hex + 2]
                for hex in range(0,
                                 len(hexdigest) - 1, 2)
            ])
        return hash.upper() + ':' + base64.b64encode(
            hashlib.new(
                hash,
                self.backend.serialize(
                    save_galois_keys=False,
                    save_relin_keys=False)).digest()).decode().replace(
                        '=', '')

    def has_private(self):
        return self.backend.is_private()

    def public_key(self):
        if not self.has_private():
            return self

        backend = self.backend.copy()
        backend.make_context_public()
        return CKKSKey(backend)


def ckks_key(*,
             coeff_modulus_bit_sizes=[52, 52, 52, 52, 52, 52, 52],
             poly_modulus_degree=16384,
             scale_bit_size=52):
    return CKKSKey(coeff_modulus_bit_sizes, poly_modulus_degree,
                   scale_bit_size)
