import numpy as np
from . import types
from .paths_and_constants import Paths


_P = Paths()
def _check_ext(fname: str, ext: str):
    if not fname.endswith(ext):
        raise ValueError(f'Expected extension "{ext}" in {fname}')


def load_npz(fname: str) -> dict[str, np.ndarray]:
    _check_ext(fname, 'npz')
    data = np.load(fname)
    return {key: data[key] for key in data.keys()}

def write_fasta(ids: types.StringArray, seqs: types.StringArray, adir: types.Path) -> None:
    with fasta_path(adir).open('w') as afile:
        for header, seq in zip(ids, seqs):
            afile.write(f'>{header}\n{seq}\n')
        



def dataset_dir(dataset:str) -> types.Path:
    return _P.data_dir / dataset
    
def datasetspec_path(adir: types.Path) -> types.Path:
    return adir / 'dataset_spec.json'

def taskspec_path(adir: types.Path, task:str) -> types.Path:
    return adir / f'{task}_spec.json'

def fasta_path(adir: types.Path) -> types.Path:
    return adir / 'proteins.fasta'

def split_path(adir: types.Path, name:str) -> types.Path:
    return adir / f'{name}_split.npz'