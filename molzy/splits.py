# Data splits.

import dataclasses
import numpy as np
import sklearn.model_selection
from . import types

@dataclasses.dataclass(frozen=True)
class SplitTuple:
    train: types.ArrayInt
    val: types.ArrayInt
    test:  types.ArrayInt

    def __post_init__(self):
        """Raises error if split parts overlap."""
        for a, b in [('train', 'val'), ('val', 'test'), ('test', 'train')]:
            overlap = np.intersect1d(getattr(self, a), getattr(self, b))
            if overlap.shape[0]:
                raise ValueError(
                    f'Found {len(overlap)} overlapping items between {a} and {b}.'
                )

    def __len__(self) -> int:
        return len(self.train) + len(self.val) + len(self.test)

    def trainval(self) -> types.DiscreteArray:
        return np.concatenate([self.train, self.val], axis=0)

    def indices(self) -> types.DiscreteArray:
        return np.concatenate([self.train, self.val, self.test], axis=0)

    def as_dict(self) -> dict[str, types.DiscreteArray]:
        return dataclasses.asdict(self)
    
    @classmethod
    def from_lists(
        cls,
        train: types.DiscreteArray,
        val: types.DiscreteArray,
        test: types.DiscreteArray
    ) -> 'SplitTuple':
        return cls(
            train=np.asarray(train),
            val=np.asarray(val),
            test=np.asarray(test)
        )
    
    def save(self, path:types.Path)-> None:
        np.savez_compressed(str(path), **self.as_dict())


def create_stratified_split(y:types.Array2D, 
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