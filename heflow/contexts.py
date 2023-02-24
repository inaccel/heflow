import functools
import joblib
import os


class CKKSContext:

    @functools.lru_cache
    def key(self):
        return joblib.load(os.getenv('HEFLOW_CKKS', 'id_ckks'))


@functools.lru_cache
def ckks_context():
    return CKKSContext()
