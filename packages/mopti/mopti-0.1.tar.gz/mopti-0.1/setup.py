from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="mopti",
    version="0.1",
    description="Multi-objective Bayesian Optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DavidWalz/mopti",
    packages=find_packages(),
    install_requires=[],
    python_requires=">=3.6",
)
