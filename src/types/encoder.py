from PIL import Image
from typing import Any, Iterable, Union
import os
import sys

if sys.version_info >= (3, 10):
    from typing import TypeAlias
else:
    from typing_extensions import TypeAlias


PathInput: TypeAlias = Union[str, os.PathLike]
PilInput: TypeAlias = Union[Image.Image, Iterable[Image.Image]]
ImageInput: TypeAlias = Union[PathInput, Iterable[PathInput], PilInput]