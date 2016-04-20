How to do a new release
=======================
Steps to create a new release:

1. check that the version bump was done in spec_cleaner/__init__.py
2. tag the new release: `git tag -s spec-cleaner-X.Y.Z`
3. upload to pypi: `python setup.py sdist upload`
4. post release version bump in spec_cleaner/__init__.py
