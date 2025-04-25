# Dataloading functionality
from __future__ import annotations
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from .paths_and_constants import Paths
import numpy as np
from .  import files
from . import types
import pandas as pd

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

    def default_dir(self)-> types.Path:
        return files.dataset_dir(self.shortname)

    def load_data(self) -> pd.DataFrame:
        df = pd.read_csv(str(self.default_dir() / self.data_file))
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

    def load_xy(self):
        df = self.dataset.load_data()
        seqs = np.unique(df[self.dataset.protein].to_numpy(str))
        smiles = np.unique(df[self.dataset.smiles].to_numpy(str))
        y = df[self.label].to_numpy(np.float32)
        return seqs, smiles, y


def load_dataset(name:str) -> DatasetSpec:
    data_dir = files.dataset_dir(name)
    dataset_path = files.datasetspec_path(data_dir)
    with dataset_path.open('r') as afile:
        dataset = DatasetSpec.from_json(afile.read())
    return dataset


def load_task(name:str, task:None) -> TaskSpec:
    data_dir = files.dataset_dir(name)
    task_path = files.taskspec_path(data_dir, task)
    with task_path.open('r') as afile:
        task = TaskSpec.from_json(afile.read())
    return task



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
        return np.savez_compressed(fname, **{key:self.mapper.index, values:self.values})

    def __call__(self, key_array: types.DiscreteArray) -> types.Array2D:
        assert isinstance(key_array, np.ndarray), 'expected np.ndarray as input!'
        return self.values[self.mapper[key_array].values]
