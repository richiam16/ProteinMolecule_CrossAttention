# Data splits.

import dataclasses
import numpy as np
import sklearn.model_selection
from . import types

@dataclasses.dataclass
class SplitTuple:
    train: types.ArrayInt
    val: types.ArrayInt
    test:  types.ArrayInt

def create_startified_split(y:types.Array2D, 
                            train_size:float, val_size:float, test_size:float, random_state=int) -> SplitTuple:
    trainval_index, test_index = sklearn.model_selection.train_test_split(
    np.arange(len(y)),
    test_size=test_size,
    random_state=random_state,
    stratify=y)
    train_index, val_index = sklearn.model_selection.train_test_split(
        trainval_index,
        test_size=val_size / (train_size + val_size),
        random_state=random_state,
        stratify=y[trainval_index],
    )
    return SplitTuple(
        train=train_index,
        val=val_index,
        test=test_index
    )