from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()
setup(
    name='pytorchkeras',
    version='0.0.2',
    description='Its a Keras replica for Pytorch',
    py_modules=["PytorchKeras", "Constants"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        'torch ~=1.7',
    ],

    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/malihamza/keras_pytorch",
    author="Ali Hamza",
    author_email="alihamzakhan94@gmail.com"
)
