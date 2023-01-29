import heflow.models
import heflow.tensors
import numpy


@heflow.models.ckks_model('decision_function')
class LogisticRegression:

    def __init__(self, model):
        self.classes_ = model.classes_
        self.he_coef_ = heflow.tensors.ckks_tensor(model.coef_).transpose_()
        self.he_intercept_ = heflow.tensors.ckks_tensor(model.intercept_)

    def decision_function(self, he_X):
        he_scores = he_X.dot_(self.he_coef_).add_(self.he_intercept_)
        return he_scores.reshape_(
            (he_scores.shape[0], )) if he_scores.shape[1] == 1 else he_scores

    def he_predict(self, X):
        he_X = heflow.tensors.ckks_tensor(X)
        he_scores = self.decision_function(he_X)
        scores = he_scores.numpy()
        if len(scores.shape) == 1:
            indices = (scores > 0).astype(int)
        else:
            indices = numpy.argmax(scores, axis=1)
        return numpy.take(self.classes_, indices, axis=0)
