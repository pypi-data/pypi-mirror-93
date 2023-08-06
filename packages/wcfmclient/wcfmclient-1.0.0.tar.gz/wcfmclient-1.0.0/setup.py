import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wcfmclient",
    author="palanskiheji",
    version="1.0.0",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    python_requires='>=2.7,!=3.0.*,!=3.1.*'
)
