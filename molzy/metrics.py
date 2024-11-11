# Evaluation related functionality.
import sklearn
import sklearn.metrics


def evaluate(y_true, y_pred, info=None):
    info = info or {}
    info['auroc'] = sklearn.metrics.roc_auc_score(y_true, y_pred)
    info['AP'] = sklearn.metrics.average_precision_score(y_true, y_pred)
    return info