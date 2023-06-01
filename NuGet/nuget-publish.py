from argparse import ArgumentParser, Namespace
import os

from NuGet.helpers.package import parse_package


def publish(file: str, source: str):
    cmd = f"dotnet nuget push \"{file}\" --source \"{source}\""

    package = parse_package(file)
    print("")
    print("*"*100)
    print(f"* Generating package for {package.name}")
    print(f"* Version {package.version}")
    print("*"*100)
    print(f"\n> {cmd}\n")

    os.system(cmd)


def main(args: Namespace):
    input = args.input
    source = args.source
    ignore = list()
    if args.ignore:
        for entry in str(args.ignore).split(","):
            ignore.append(entry.strip())
    
    

    print("\n>> Done")


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('-i', '--input', required=True,
                        help='Input path of the package to publish')

    parser.add_argument('-s', '--source', required=True,
                        help='NuGet package source URL')

    parser.add_argument("auto",
                        help="Interprets the input as a directory which can contain multiple packages therefore recurses through it.")

    parser.add_argument("-v", "--version", type=str,
                        help="Version number of the package. If left empty, takes the latest.")

    parser.add_argument("-ig", "--ignore", type=str,
                        help="Which projects shall be ignored (Specify as comma separated values) >> Supports wildcards! <<")

    main(parser.parse_args())
