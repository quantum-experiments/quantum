from setuptools import setup, find_packages
setup(
    name="quantum",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "parsimonious"
    ],
    extras_require={
        "examples": ["matplotlib", "jupyter"],
        "dev": ["pytest", "jupytext"]
    }
)