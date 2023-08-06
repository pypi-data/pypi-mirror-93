
from setuptools import setup
from setuptools import find_packages
import ixten


with open("requirements.txt") as iF:
    requirements = iF.read().splitlines()


setup(
    name='ixten',
    version=ixten.__version__,
    author='Félix Brezo (@febrezo)',
    description='A tool to verify whether some ports are opened or not',
    include_package_data=True,
    license='GNU GPLv3+',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'ixten=ixten.cli:main',
        ],
    },
    install_requires=requirements
)
