# Types and enums.
from typing import Sequence
from jaxtyping import Float, Integer
from torch import Tensor
import numpy as np
from enum import StrEnum, auto

Array = Tensor | np.ndarray
ArrayInt = Integer[Array, 'n']
DiscreteArray = ArrayInt | Sequence[str]
Array2D = Float[Array, 'n k']


class EmbeddingStyle(StrEnum):
    """Token or global embedding?"""
    token = auto()
    globals = auto()