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

DEFAULT_PROT_INDEX = 'prot_id'

@dataclass_json
@dataclass(frozen=True)
class DatasetSpec:
    """Specification for a dataset with potentially many tasks."""
    name: str
    shortname: str
    data_file: types.Path
    labels: list[str] 
    columns: dict[str, str]
    protein: str ='sequence'
    protid: str = DEFAULT_PROT_INDEX
    smiles: str='isosmiles'
    doi: str = ''
    comments : str = ''

    def load_dataset(self) -> pd.DataFrame:
        data_path = files.dataset_dir(self.shortname) / self.data_file
        df = pd.read_csv(str(data_path))
        return df



@dataclass_json
@dataclass(frozen=True)
class TaskSpec:
    """Specification for an ML task."""
    dataset: DatasetSpec
    label: str
    task_type: types.TaskType
    units : str
    standard_split: str
    available_splits: list[str]


def load_dataset(name:str) -> tuple[DatasetSpec, pd.DataFrame]:
    spec_path = Path(_P.data_dir / name / 'dataspec.json')
    with spec_path.open('r') as afile:
     spec = DatasetSpec.from_json(afile.read())

    data_path = Path(_P.data_dir / name / f'{name}_data.csv')
    df = pd.read_csv(str(data_path))
    return spec, df




class ArrayMap:
    """Map discrete values (sequences, int, smiles) to arrays."""

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
