from argparse import ArgumentParser, Namespace
from fnmatch import fnmatch
import os
import shutil
import re
from typing import List, Optional
import packaging.version as pv

from NuGet.helpers import versiontool as vt

project_files = [
    "csproj",          # - C#
    "vbproj",          # - Visual Basic
    "vcxproj",         # - C++
    "fsproj",          # - F#
    "wapproj",         # - Windows Phone App
    "xapdeployproj",   # - Windows Phone deployment
    "njsproj",         # - Node.js
    "sqlproj",         # - SQL Server
    "shproj",          # - Shared
]


def matches_any(arg: str, patterns: List[str]) -> bool:
    for pattern in patterns:
        if fnmatch(arg, pattern):
            return True

    return False


def pack(input_dir: str, output_dir: str, version_map: Optional[dict[str, str]] = None, static_version: Optional[str] = None, ignore: Optional[List[str]] = None) -> None:
    for item in os.listdir(input_dir):
        path = os.path.join(input_dir, item)

        if os.path.isdir(path):
            # Recurse
            pack(path, output_dir, version_map, static_version, ignore)
            continue

        file_parts = item.rsplit('.', 1)

        # ignore extension-less files rightaway
        if len(file_parts) < 2:
            continue

        file_name, file_extension = file_parts

        if ignore and matches_any(file_name, ignore):
            continue

        if static_version is not None:
            version = static_version
        else:
            if file_name in version_map:
                version = version_map[file_name]
            else:
                version = "0.0.1"

        if file_extension in project_files:
            cmd = f"nuget pack \"{path}\" -version {version}"
            print("")
            print("*"*100)
            print(f"* Generating package for {file_name}")
            print(f"* Version {version}")
            print("*"*100)
            print(f"\n> {cmd}\n")
            os.system(cmd)
            shutil.move(f"{file_name}.{version}.nupkg", output_dir)


def main(args: Namespace):
    input_dir = args.input_dir
    output_dir = args.output_dir
    ignore = list()
    if args.ignore:
        for entry in str(args.ignore).split(","):
            ignore.append(entry.strip())

    if args.version:
        pack(input_dir, output_dir, static_version=args.version, ignore=ignore)

    elif args.autoversion:
        increment = "0.0.1" if not args.autoversion_increment else args.autoversion_increment
        cur_versions = vt.get_latest(output_dir)
        incr_versions = vt.increment_versions(cur_versions, increment)
        pack(input_dir, output_dir, ignore=ignore, version_map=incr_versions)

    print("\n>> Done")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-i", "--input_dir", type=str, required=True,
                        help="Directory that contains the projects to make nuget packages from")

    parser.add_argument("-o", "--output_dir", type=str, required=True,
                        help="Directory that the nuget packages shall be saved to")

    parser.add_argument("autoversion",
                        help="Uses the output directory and memorizes version information from the packages there."
                        "\nThat version number + some increment (default=0.0.1) will be the resulting package version")

    parser.add_argument("-avi", "--autoversion_increment", type=str,
                        help="Version number by which shall be incremented")

    parser.add_argument("-v", "--version", type=str,
                        help="Version number of the generated packages.")

    parser.add_argument("-ig", "--ignore", type=str,
                        help="Which projects shall be ignored (Specify as comma separated values) >> Supports wildcards! <<")

    main(parser.parse_args())
