import os
from pathlib import Path
from typing import Callable, Iterable, Tuple, Union, Any


Rename = Union[None, Callable[[Path], Union[str, Path]]]


class InvalidDirectoryError(Exception):
    pass


def _ensure_dir(dir_path: Union[str, Path], must_exist=True) -> Path:
    """
    Convert str to Path. Check if directory exists and contains no invalid symbols.
    """
    dir_path = Path(dir_path)
    s = str(dir_path)
    if '*' in s or '?' in s:
        raise InvalidDirectoryError(f'Path contains invalid symbols: {dir_path}')
    if dir_path.exists():
        if not dir_path.is_dir():
            raise NotADirectoryError(f'Not a directory: {dir_path}')
    elif must_exist:
        raise FileNotFoundError(f'Directory not found: {dir_path}')
    return dir_path


def iter_files(dir_path: Union[str, Path], pattern: str = '**/*') -> Iterable[Path]:
    """
    Iterates over file names in dir_path.

    Use glob pattern to filter; by default, all files in all subdirectories are included.
    """
    dir_path = _ensure_dir(dir_path)
    # NOTE: we must do list() to take a "snapshot" of all files at a given moment.
    # This is to ensure predictable behavior.
    for file_path in list(dir_path.glob(pattern)):
        if not file_path.is_file():
            continue
        yield file_path


def iter_texts(dir_path: Union[str, Path], pattern: str = '**/*', encoding=None, errors=None) -> Iterable[str]:
    """
    Iterates over text file contents (as str) in dir_path.

    Use glob pattern to filter; by default, all files in all subdirectories are included.
    If necessary, specify encoding and errors to pass to ``Path.read_text()``.
    """
    for file_path in iter_files(dir_path, pattern):
        yield file_path.read_text(encoding=encoding, errors=errors)


def for_each_file(dir_path: Union[str, Path], function: Callable[[Path], Any], pattern: str = '**/*') -> None:
    """
    Calls function for each file in dir_path.

    Use glob pattern to filter; by default, all files in all subdirectories are included.
    """
    for file_path in iter_files(dir_path, pattern):
        function(file_path)


def for_each_text(dir_path: Union[str, Path], function: Callable[[str], Any], pattern: str = '**/*', encoding=None, errors=None) -> None:
    """
    Calls function for each file contents (as str) in dir_path.

    Use glob pattern to filter; by default, all files in all subdirectories are included.
    If necessary, specify encoding and errors to pass to ``Path.read_text()``.
    """
    for file_path in iter_texts(dir_path, pattern, encoding, errors):
        function(file_path)


def iter_convert(source_dir: Union[str, Path], target_dir: Union[str, Path], pattern: str = '**/*', rename: Rename = None) -> Iterable[Tuple[Path, Path]]:
    """
    Creates the same hierarchy of subdirectories in target_dir as in source_dir.
    Iterates over pairs: each file in source_dir, and corresponding file in target_dir.
    """
    # Make sure caller is not messing up the directory structure.
    source_dir = _ensure_dir(source_dir)
    target_dir = _ensure_dir(target_dir, must_exist=False)
    if target_dir in source_dir.parents or source_dir in target_dir.parents:
        raise InvalidDirectoryError('Source must not be a parent of Target (and vice versa)')

    parents = set()  # optimize os.makedirs for "thousands of files in a folder" scenario

    for source_file_path in iter_files(source_dir, pattern):
        target_file_path = target_dir / source_file_path.relative_to(source_dir)
        if rename:
            new_name = rename(target_file_path)
            target_file_path = target_file_path.parent / (new_name.name if type(new_name) is Path else new_name)
        if target_file_path.parent not in parents:
            os.makedirs(target_file_path.parent, exist_ok=True)
            parents.add(target_file_path.parent)
        yield source_file_path, target_file_path


def convert_files(source_dir: Union[str, Path], target_dir: Union[str, Path], function: Callable[[Path, Path], Any], pattern: str = '**/*', rename: Rename = None) -> None:
    """
    Creates the same hierarchy of subdirectories in target_dir as in source_dir.
    Calls function for each pair of files (in source_dir and a corresponding file in target_dir).

    By default, target file has the same name and extension; specify ``rename`` callable to change target file name.
    """
    for source_file_path, target_file_path in iter_convert(source_dir, target_dir, pattern, rename):
        function(source_file_path, target_file_path)


def convert_texts(source_dir: Union[str, Path], target_dir: Union[str, Path], function: Callable[[str, Path], Any], pattern: str = '**/*', rename: Rename = None, encoding=None, errors=None) -> None:
    """
    Creates the same hierarchy of subdirectories in target_dir as in source_dir.
    Calls function for each file content (as str) in source_dir,
    and writes result (as str) into corresponding file in target_dir.

    By default, target file has the same name and extension; specify ``rename`` callable to change target file name.
    """
    for source_file_path, target_file_path in iter_convert(source_dir, target_dir, pattern, rename):
        target_file_path.write_text(function(source_file_path.read_text(encoding=encoding, errors=errors)), encoding=encoding, errors=errors)
