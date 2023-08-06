import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="uqoclient",
    version="1.0.3",
    author="QAR-Lab Munich",
    author_email="Sebastian.Zielinski@ifi.lmu.de",
    description="Client of the optimisation framework UQO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    install_requires=[
        'dimod==0.9.10',
        'dwave-networkx==0.8.8',
        'prettytable==0.7.2',
        'pyzmq==20.0.0',
        'matplotlib==3.3.2'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)