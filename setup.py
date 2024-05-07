from setuptools import setup, find_packages

setup(
    name="arc2",
    version="0.1.0",
    description="Prototype for ARC project",
    author="Jeremy Magland",
    author_email="jmagland@flatironinstitute.org",
    packages=find_packages(),
    install_requires=[
        "click>=8.1.7",
    ],
    entry_points={
        "console_scripts": [
            "arc2 = arc2.cli:main",
        ],
    },
)