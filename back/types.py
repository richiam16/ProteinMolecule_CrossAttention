# Types and enums.
from typing import Sequence
from jaxtyping import Float, Integer
from torch import Tensor
import numpy as np
import pathlib
from enum import StrEnum, auto

StringArray = Sequence[str]
Array = Tensor | np.ndarray
ArrayInt = Integer[Array, 'n']
DiscreteArray = ArrayInt | StringArray
Array2D = Float[Array, 'n k']

Path = pathlib.Path

class EmbeddingStyle(StrEnum):
    """Token or global embedding?"""
    token = auto()
    globals = auto()

class TaskType(StrEnum):
    """Type of task."""
    regression = auto()
    binary = auto()