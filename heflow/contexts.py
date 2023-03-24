from mlflow.tracking.context.abstract_context import RunContextProvider

import functools
import heflow
import os


class CKKSContext(RunContextProvider):

    def in_context(self):
        try:
            self.key()
        except Exception:
            return False
        return True

    @classmethod
    @functools.lru_cache
    def key(cls):
        return heflow.load_key(os.getenv('HEFLOW_CKKS', 'id_ckks'))

    def tags(self):
        return {'heflow.ckks_key.fingerprint': self.key().fingerprint()}
