## nuget-pack.py
Recursively iterates through given directory and generates a nuget package for every project. \
The nuget package file is then moved to a given output directory.

Usage:
```
python nuget-pack.py -i where/your/projects/are -o where/the/packages/should/go [-v "x.y.z"] [autoversion] [-avi "x.y.z"]
```

When you use the autoversion option, it will look for the latest package version in the output directory and use that version + given increment (0.0.1 if not set) for the package that is to be generated.
