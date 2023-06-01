import os
import re
import packaging.version as pv


def get_latest(dir: str) -> dict[str, str]:
    """
    Gets the latest packages from a directory.

    Returns:
        Dictionary with package name as keys and version as values
    """
    version_dict = {}

    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)

        if os.path.isfile(file_path) and file_name.endswith('.nupkg'):
            pattern = r"(?P<name>.+)\.(?P<version>\d+\.\d+\.\d+)\.(?P<extension>.+)"
            match = re.match(pattern, file_name)

            if not match:
                continue

            name = match.group("name")
            version = match.group("version")

            if name in version_dict and pv.Version(version) <= pv.Version(version_dict[name]):
                continue

            version_dict[name] = version

    return version_dict


def increment_version(version: str, increment: str) -> str:
    version_components = version.split('.')
    increment_components = increment.split('.')

    # pad the version and increment components with zeros if needed
    while len(version_components) < len(increment_components):
        version_components.append('0')
    while len(version_components) > len(increment_components):
        increment_components.append('0')

    # add the corresponding components of the two version numbers
    new_version_components = []
    for i in range(len(version_components)):
        new_version_components.append(
            str(int(version_components[i]) + int(increment_components[i])))

    # join the components into a new version number
    new_version = '.'.join(new_version_components)

    return new_version


def increment_versions(version_dict: dict[str, str], increment: str) -> dict[str, str]:
    for name, version in version_dict.items():
        version_dict[name] = increment_version(version, increment)

    return version_dict
