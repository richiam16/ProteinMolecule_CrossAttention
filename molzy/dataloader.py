# Dataloading functionality
from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .paths_and_constants import Paths
import numpy as np
from .  import files
from . import types
import pandas as pd
from pathlib import Path

_P = Paths()

class ArrayMap:

    def __init__(self, keys:types.DiscreteArray, values:types.Array2D):

        self.mapper = pd.Series(data=np.arange(len(keys)), index=keys)
        self.values = values
        # Check for duplicates.
        dups = self.mapper.index[self.mapper.index.duplicated()].tolist()
        if dups:
            raise ValueError(f'Found {len(dups)} duplicated isosmiles={dups}')
    
    @classmethod
    def load(cls, fname:str, key: str = 'isosmiles', values: str = 'values') -> ArrayMap:
        data = files.load_npz(fname)
        assert key in data, f'{key} not found in {data.keys()}'
        assert values in data, f'{values} not found in {data.keys()}'
        return ArrayMap(data[key], data[values])

    def save(self, fname:str, key: str = 'isosmiles', values: str = 'values'):
        return np.savez_compressed(fname, key=self.mapper.keys, values=values)

    def __call__(self, key_array: types.DiscreteArray) -> types.Array2D:
        assert isinstance(key_array, np.ndarray), 'expected np.ndarray as input!'
        return self.values[self.mapper[key_array].values]
    
@dataclass_json
@dataclass(frozen=True)
class DataSpec:
    name: str
    label: str
    protein: str='sequence'
    protid: str = ''
    smiles: str='isosmiles'
    context : str = ''


def load_dataset(name:str) -> tuple[DataSpec, pd.DataFrame]:
    spec_path = Path(_P.data_dir / name / 'dataspec.json')
    with spec_path.open('r') as afile:
     spec = DataSpec.from_json(afile.read())

    data_path = Path(_P.data_dir / name / f'{name}_data.csv')
    df = pd.read_csv(str(data_path))
    return spec, df