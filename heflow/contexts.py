from mlflow.tracking.context.abstract_context import RunContextProvider

import functools
import joblib
import os


class CKKSContext(RunContextProvider):

    def in_context(self):
        try:
            self.key()
        except Exception:
            return False
        return True

    @functools.lru_cache
    def key(self):
        return joblib.load(os.getenv('HEFLOW_CKKS', 'id_ckks'))

    def tags(self):
        return {'heflow.ckks_key.fingerprint': self.key().fingerprint()}


@functools.lru_cache
def ckks_context():
    return CKKSContext()
