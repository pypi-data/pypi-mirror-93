# See description in CONTRIBUTING.md

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siasearch",
    version="0.0.7",
    author="Timofey Molchanov",
    author_email="timofey.molchanov@merantix.com",
    description="SDK for SiaSearch platform API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://demo.sia-search.com/sdk_docs/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["dataclasses", "ipython", "pandas", "matplotlib", "scikit-image", "requests", "pyarrow"],
    python_requires=">=3.6",
)
