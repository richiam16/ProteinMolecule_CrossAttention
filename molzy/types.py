# Types and enums.

from jaxtyping import Array, Float, Integer

from enum import StrEnum, auto

ArrayInt = Integer[Array, 'n']
Array2D = Float[Array, 'n k']


class EmbeddingStyle(StrEnum):
    """Token or global embedding?"""
    token = auto()
    globals = auto()