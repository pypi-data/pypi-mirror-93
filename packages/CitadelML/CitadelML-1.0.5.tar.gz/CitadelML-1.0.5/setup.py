import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="CitadelML",
    version="1.0.5",
    author="Cody Richter",
    author_email="cody@richter.codes",
    description="Upload and train machine learning models on a remote server.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/UMass-Rescue/PhotoAnalysisServer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'requests'
    ],
    python_requires='>=3.0',
)
