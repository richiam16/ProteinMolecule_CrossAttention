# Types and enums.

import jaxtyping
from jaxtyping import Array, Float, Integer

from enum import StrEnum, auto

ArrayInt = Int[Array, 'n']
Array2D = Float[Array, 'n k']


class EmbeddingStyle(StrEnum):
    """Token or global embedding?"""
    token = auto()
    globals = auto()