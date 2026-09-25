How to do a new release
=======================
Steps to create a new release:

1. Check that the version bump was done in `spec_cleaner/__init__.py`.
2. Run `make` to verify the generated data are up-to-date.
3. Tag the new release: `git tag -s spec-cleaner-X.Y.Z`.
4. Push the tag: `git push origin spec-cleaner-X.Y.Z`.

Pushing the tag triggers the `Release to PyPI` GitHub Actions workflow, which:
- verifies the tag version matches `spec_cleaner.__version__`,
- verifies the generated data are up-to-date (`make` must produce no diff),
- builds the sdist and wheel,
- uploads them to PyPI,
- creates a GitHub Release with auto-generated notes.

5. Post release version bump in `spec_cleaner/__init__.py`.
