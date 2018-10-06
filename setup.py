import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bls_datasets",
    version="0.0.2",
    author="Maxim Kupfer",
    author_email="mbkupfer@gmail.com",
    description="Python library for retrieving BLS datasets",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbkupfer/bls-datasets",
    packages=['bls_datasets'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
