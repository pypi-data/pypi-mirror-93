from setuptools import find_packages, setup

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="noiser",
    version="0.0.0",
    author="Jake Tae",
    author_email="jaesungtae@gmail.com",
    description="Text noise corruption for language model pretraining",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jaketae/noiser",
    packages=find_packages(exclude=["docs", "tests"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[],
)
