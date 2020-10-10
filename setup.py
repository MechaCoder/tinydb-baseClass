from setuptools import setup, find_packages

file = open('readme.md', 'r')
longDisc = file.read()
file.close()

setup(
    name='tinydb-baseClass',
    version='0.2.3',
    description='a base class to tinydb',
    long_description=longDisc,
    long_description_content_type="text/markdown",
    author='postitnotenija',
    url='https://github.com/MechaCoder/tinyDbBase',
    py_modules=['tinydb_base'],
    packages=find_packages(),
    install_requires=['tinydb', 'cryptography', 'pyyaml'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
    ]
)
