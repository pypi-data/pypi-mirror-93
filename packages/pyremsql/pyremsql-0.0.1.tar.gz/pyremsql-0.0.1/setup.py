from setuptools import setup
from os import path

curdir = path.abspath(path.dirname(__file__))  # the directory where the file is located
readme_fp = path.join(curdir, "README.md")  # the path where the README is located
require_fp = path.join(curdir, "requirements.txt")  # the path where the requirements are located

with open(readme_fp, "r") as f:  # read the readme and put it into the long description for later
    long_desc = f.read()

with open(require_fp, "r") as f:  # read and split the requirements in requirements.txt
    require = f.read().split("\n")

setup(
    name='pyremsql',
    version='0.0.1',
    packages=['pyremsql'],
    install_requires=require,
    python_requires=">=3.6, <4",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    license='GPL3',
    url='https://github.com/XazkerBoy/RemoteSQLite',
    author='Xazker',
    author_email='xazkerboy@gmail.com',
    description='Python wrapper for RemoteSQLite API'
)
