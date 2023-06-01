from dataclasses import dataclass
import os
import re


@dataclass
class NuGetPackage():
    name: str
    version: str


def parse_components(file: str) -> tuple[str, str]:
    file_name = os.path.basename(file)
    pattern = r"(?P<name>.+)\.(?P<version>\d+\.\d+\.\d+)\.(?P<extension>.+)"
    match = re.match(pattern, file_name)

    if not match:
        raise Exception(f"Not a nuget package: {file}")

    name = match.group("name")
    version = match.group("version")

    return name, version


def parse_package(file: str) -> NuGetPackage:
    name, version = parse_components(file)

    return NuGetPackage(name, version)
