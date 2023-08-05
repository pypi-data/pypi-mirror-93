from os import PathLike
from typing import Callable, Optional, Iterable, Union
from zipfile import ZipFile

from .types import Path


def save_tests(
    inputs: Iterable[str],
    outputs: Iterable[str],
    filename: Path = "tests.zip",
):
    zipfile: ZipFile
    with ZipFile(filename, "w") as zipfile:
        i: int
        input_: str
        output: str
        for i, (input_, output) in enumerate(zip(inputs, outputs)):
            _write_test_to_zipfile(zipfile, i, input_, output)


def make_and_save_tests(
    inputs: Iterable[str],
    solve_func: Callable[[str], str],
    filename: Path = "tests.zip",
):
    zipfile: ZipFile
    with ZipFile(filename, "w") as zipfile:
        i: int
        input_: str
        output: str
        for i, input_ in enumerate(inputs):
            _write_test_to_zipfile(zipfile, i, input_, solve_func(input_))


def _write_test_to_zipfile(
    zipfile: ZipFile, test_number: Union[int, str], input_: str, output: str
):
    zipfile.writestr(f"input/input{test_number:02}.txt", input_)
    zipfile.writestr(f"output/output{test_number:02}.txt", output)
