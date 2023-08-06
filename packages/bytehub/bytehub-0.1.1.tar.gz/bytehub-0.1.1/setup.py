from setuptools import setup, find_packages
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_desc = f.read()

with open(path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    install_requires = f.read()

exec(open('bytehub/version.py').read())

setup(
    name='bytehub',
    packages=find_packages(),
    version=__version__,
    description='Python SDK for ByteHub timeseries feature store',
    author='ByteHub AI Limited',
    url='https://bytehub.ai',
    long_description=long_desc,
    long_description_content_type='text/markdown',
    install_requires=install_requires,
    extras_require={
        'dev': [
            'pytest',
            'autopep8',
        ]
    }
)
