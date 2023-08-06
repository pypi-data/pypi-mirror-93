import setuptools

with open("README.md", 'r') as fh:
    long = fh.read()

attrs = {
    "name": "PapTcpg",
    "version": "1.6.0",
    "author": "RapperXandSheepW",
    "packages": setuptools.find_packages(),
    "include_package_data": True,
    "platforms": 'any',

}

setuptools.setup(**attrs)
