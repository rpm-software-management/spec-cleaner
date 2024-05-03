"""Setup.py file describing default values and contact information."""
from glob import glob

from setuptools import setup

from spec_cleaner import __version__

setup(
    name='spec_cleaner',
    description='RPM .spec files cleaner',
    long_description=(
        'Command-line tool for cleaning various formatting errors in RPM .spec files'
    ),
    url='https://github.com/rpm-software-management/spec-cleaner',
    download_url='https://github.com/rpm-software-management/spec-cleaner',
    version=__version__,
    author='Tomáš Chvátal',
    author_email='tchvatal@suse.com',
    maintainer='Tomáš Chvátal',
    maintainer_email='tchvatal@suse.com',
    license='License :: OSI Approved :: BSD License',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: Unix',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Utilities',
        'Topic :: Text Processing',
    ],
    platforms=['Linux'],
    keywords=['SUSE', 'RPM', '.spec', 'cleaner'],
    tests_require=['pytest', 'pytest-cov', 'pytest-xdist'],
    install_requires=['python-rpm-spec'],
    packages=['spec_cleaner'],
    data_files=[('lib/obs/service/', glob('obs/*')), ('share/spec-cleaner', glob('data/*'))],
    entry_points={'console_scripts': ['spec-cleaner = spec_cleaner:main']},
)
