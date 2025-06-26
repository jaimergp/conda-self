import configparser
from pathlib import Path

from conda.exceptions import CondaError


class MultipleDistInfoDirsFound(CondaError):
    pass


class NoDistInfoDirFound(CondaError):
    pass


# This is required for reading entry point info from an extracted package
# ref: https://packaging.python.org/en/latest/specifications/entry-points/#file-format
class CaseSensitiveConfigParser(configparser.ConfigParser):
    optionxform = staticmethod(str)


class PackageInfo:
    def __init__(self, dist_info_path: Path):
        """Describe the dist-info for a conda package"""
        self.dist_info_path = dist_info_path

    @classmethod
    def from_conda_extracted_package_path(cls, path: str):
        """Create a PackageInfo object given the path to an extracted conda package"""
        path = Path(path)
        matching_paths = [
            p for p in path.rglob("**/*site-packages/*dist-info*") if p.is_dir()
        ]
        if len(matching_paths) > 1:
            raise MultipleDistInfoDirsFound()
        elif len(matching_paths) == 0:
            raise NoDistInfoDirFound()
        return cls(matching_paths[0])

    def entry_points(self) -> dict[str, dict[str, str]]:
        """Get the entry points for a package.

        The return value for this function has the form:

        {
            entry_point_group:{
                name: entry_point,
                . . .
            }
            . . .
        }

        :returns: a dictionary of entry point groups and the corresponding entry points
                  expressed as a dict.

        ref: https://packaging.python.org/en/latest/specifications/entry-points/#file-format
        """
        entry_point_file = self.dist_info_path / "entry_points.txt"
        entry_points_config = CaseSensitiveConfigParser()
        entry_points_config.read(entry_point_file)

        entry_points = {}
        for section in entry_points_config.sections():
            entry_points[section] = dict(entry_points_config[section])

        return entry_points
