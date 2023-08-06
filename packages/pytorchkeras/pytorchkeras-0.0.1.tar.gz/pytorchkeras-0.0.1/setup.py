from setuptools import setup

setup(
    name='pytorchkeras',
    version='0.0.1',
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

    url="https://github.com/malihamza/keras_pytorch",
    author="Ali Hamza",
    author_email="alihamzakhan94@gmail.com"
)
