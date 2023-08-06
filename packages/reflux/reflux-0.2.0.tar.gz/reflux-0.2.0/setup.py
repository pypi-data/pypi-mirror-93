import setuptools

from reflux import __version__

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="reflux",
    version=__version__,
    author="IreTheKID",
    author_email="author@example.com",
    description="Python package for creating IDE themes on Repl.it. Uses JavaScript bookmarlets!",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IreTheKID/Reflux",
    packages=["reflux"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
