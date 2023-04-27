from argparse import ArgumentParser, Namespace
import os
import shutil
import re
import packaging.version as pv

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


def increment_versions(version_map: dict[str, str], increment: str) -> dict[str, str]:
    for name, version in version_map.items():
        version_map[name] = increment_version(version, increment)

    return version_map


def gather_versions(dir: str) -> dict[str, str]:
    version_map = {}

    for file_name in os.listdir(dir):
        file_path = os.path.join(dir, file_name)

        if os.path.isfile(file_path) and file_name.endswith('.nupkg'):
            pattern = r"(?P<name>.+)\.(?P<version>\d+\.\d+\.\d+)\.(?P<extension>.+)"
            match = re.match(pattern, file_name)

            if not match:
                continue

            name = match.group("name")
            version = match.group("version")

            if name in version_map and pv.Version(version) <= pv.Version(version_map[name]):
                continue

            version_map[name] = version

    return version_map


def pack(input_dir: str, output_dir: str, version_map: dict[str, str] = None, static_version: str = None) -> None:
    for item in os.listdir(input_dir):
        path = os.path.join(input_dir, item)

        if os.path.isdir(path):
            # Recurse
            pack(path, output_dir, version_map, static_version)
            continue

        file_parts = item.rsplit('.', 1)

        # ignore extension-less files rightaway
        if len(file_parts) < 2:
            continue

        file_name, file_extension = file_parts

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

    if args.version:
        pack(input_dir, output_dir, static_version=args.version)

    elif args.autoversion:
        increment = "0.0.1" if not args.autoversion_increment else args.autoversion_increment
        pack(input_dir, output_dir, version_map=increment_versions(gather_versions(output_dir), increment))
    
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

    main(parser.parse_args())
