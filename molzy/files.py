import numpy as np


def _check_ext(fname: str, ext: str):
    if not fname.endswith(ext):
        raise ValueError(f'Expected extension "{ext}" in {fname}')


def load_npz(fname: str) -> dict[str, np.ndarray]:
    _check_ext(fname, 'npz')
    data = np.load(fname)
    return {key: data[key] for key in data.keys()}
