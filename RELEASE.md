How to do a new release
=======================
Steps to create a new release:

1. check that the version bump was done in spec_cleaner/__init__.py
2. run `make` to verify the generated data are up-to-date
3. tag the new release: `git tag -s spec-cleaner-X.Y.Z`
4. verify travis did upload new version to to pypi
5. post release version bump in spec_cleaner/__init__.py
