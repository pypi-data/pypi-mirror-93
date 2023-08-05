import setuptools

with open('requirements.txt') as f:
    requirements = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gpval",  # geopackage_validator
    author="MC",
    description="geopackages validator utility",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MapColonies/geopackage_validator.git",
    packages=setuptools.find_packages(),
    install_requires=requirements,
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)