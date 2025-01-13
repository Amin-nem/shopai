from PIL import Image
from typing import Iterable, Union
import os
from typing import TypeAlias

PathInput: TypeAlias = Union[str, os.PathLike]
PilInput: TypeAlias = Union[Image.Image, Iterable[Image.Image]]
ImageInput: TypeAlias = Union[PathInput, Iterable[PathInput], PilInput]
