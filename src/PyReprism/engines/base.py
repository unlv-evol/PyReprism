"""Backend abstraction: an engine turns source into a typed token stream."""
from typing import List

from ..tokens import Token


class Engine:
    """Base class for tokenization backends.

    An engine only has to implement :meth:`tokenize`; every higher-level
    operation (remove/extract/count/normalize/stats) is derived from the token
    stream by :mod:`PyReprism._tokenops`.
    """

    name = 'base'

    def tokenize(self, source: str, language_cls) -> List[Token]:
        raise NotImplementedError
