How to do a new release
=======================
Steps to create a new release:

1. Check that the version bump was done in `spec_cleaner/__init__.py`.
2. Run `make` to verify the generated data are up-to-date.
3. Tag the new release: `git tag -s spec-cleaner-X.Y.Z`.
4. Push the tag and release the new version: `git push origin spec-cleaner-X.Y.Z`.
5. Upload the new version to PyPi `python3 setup.py sdist upload`.
6. Post release version bump in `spec_cleaner/__init__.py`.
