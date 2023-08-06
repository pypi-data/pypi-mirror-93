from pathlib import PurePath
from typing import List

from pkg_resources import resource_listdir, resource_filename


def get_folder(root_pkg_name: str = __package__, migration_dir: str = "migrations") -> PurePath:
    """
    Retrieve folder in module: root_pkg_name.directory
    """
    path = resource_filename(root_pkg_name, migration_dir)
    return path


def get_files(root_pkg_name: str = __package__, directory: str = "migrations") -> List[PurePath]:
    """
    Retrieve list of files in module: root_pkg_name.directory
    """
    paths = resource_listdir(root_pkg_name, directory)
    return paths
