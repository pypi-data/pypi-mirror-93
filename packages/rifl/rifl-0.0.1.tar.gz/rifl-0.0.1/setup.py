"""Setup script for rifl."""
from setuptools import setup, find_packages, Command
from shutil import rmtree
import codecs
import io
import os
import sys

here = os.path.abspath(os.path.dirname(__file__))

def read(*parts):
    """Return multiple read calls to different readable objects as a single string."""
    return codecs.open(os.path.join(here, *parts), 'r').read()

NAME = 'rifl'
DESCRIPTION = f'{NAME} is a data filtration library for MS-proteomics experiments.'
LONG_DESCRIPTION = read('README.md')
URL = 'https://github.com/radusuciu/rifl'
EMAIL = 'radusuciu@gmail.com'
AUTHOR = 'Radu Suciu'

# not doing import because do not want to have to load module
# before it has been installed
version_path = os.path.join(here, 'rifl/version.py')
exec(read(version_path))
VERSION = __version__

REQUIRED = [
    'beautifulsoup4',
    'biopython',
    'click',
    'pandas',
    'peewee',
    'pyyaml',
    'requests',
    'numpy',
    'scipy',
]


# from github.com/kennethreitz/setup.py
class UploadCommand(Command):
    """Support setup.py upload."""

    description = 'Build and publish the package.'
    user_options = []

    @staticmethod
    def status(s):
        """Prints things in bold."""
        print('\033[1m{0}\033[0m'.format(s))

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        sys.exit()


setup(
    name=NAME,
    version=VERSION,
    url=URL,
    author=AUTHOR,
    author_email=EMAIL,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.2',
    packages=find_packages(exclude=('tests',)),
    install_requires=REQUIRED,
    entry_points={
        'console_scripts': ['rifl=rifl.cli:main']
    },
    include_package_data=True,
    platforms='any',
    zip_safe=True,
    license='MIT License',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Natural Language :: English',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
    ],
    # $ setup.py publish support.
    cmdclass={
        'upload': UploadCommand,
    },
)