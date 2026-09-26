How to do a new release
=======================
Releases are cut from master. The `Create signed release tag` workflow signs
the tag and starts the `Release to PyPI` workflow, which tests, builds and
publishes the release. Building rpm or deb packages is not part of it.

Before the first release
------------------------
Set up once:
- a GitHub trusted publisher on PyPI for this repository, the workflow
  `release.yml` and the environment `pypi`, added by a PyPI owner, who also
  removes any other publisher; API tokens belong to PyPI accounts, so whoever
  made one for this project revokes it once it is unused,
- the signing subkey secrets that `create-release-tag.yml` reads, and the
  matching public key, signing subkey included, on the GitHub account whose
  key `release.yml` imports to verify the tag.

The first release run creates the `pypi` environment with no rules. Until a
repository admin adds the release managers as its required reviewers and
limits its deployments to `spec-cleaner-*` tags, anyone with write access can
publish.

Each release manager needs write access to run the tagging workflow, and must
be a reviewer of the `pypi` environment if it has any.

The signing subkey expires; `gpg --show-keys` on the key that `release.yml`
downloads shows when. Before then, the key's owner extends it and replaces the
key on GitHub (delete the old one, then add the new export), and someone with
write access replaces the subkey secret with the new
`gpg --armor --export-secret-subkeys <subkey ID>!`. Without the new secret the
tagging workflow cannot sign, and without the new key `release.yml` cannot
verify the tag. A release manager who signs with a key of their own puts its
signing subkey in the secrets, its public key on their GitHub account, and
their account in the key URL in `release.yml`.

Versions
--------
Bump the minor version when the default output, the command line options or
the supported Python versions change, and the patch version for fixes and data
refreshes. After a release, master carries the next patch version.

Steps
-----
1. Run `make` on master. If it changes anything, merge that refresh first, as
   the release checks that `make` leaves no diff.
2. Check that `spec_cleaner/__init__.py` has the version to release, and bump
   it in a pull request if not.
3. Run the `Create signed release tag` workflow on master (Actions tab, or
   `gh workflow run create-release-tag.yml --ref master`). It tags
   `spec-cleaner-X.Y.Z` and starts `Release to PyPI` for it.
4. The release workflow runs the tests, verifies the tag signature, checks
   that the tag matches `spec_cleaner.__version__` and that `make` leaves no
   diff, and builds the sdist and wheel.
5. If the `pypi` environment requires a review, approve the deployment in the
   workflow run. The sdist and wheel are uploaded to PyPI, and a GitHub
   release is created with generated notes and the same files attached.
   Optionally add a short summary above the notes.
6. Post release version bump in `spec_cleaner/__init__.py`.

Checking a release
------------------
- Each file under "Download files" on https://pypi.org/project/spec-cleaner/
  shows its provenance: this repository, `release.yml` and the release tag.
- `uvx --from spec-cleaner==X.Y.Z spec-cleaner --version` prints X.Y.Z.

When it fails
-------------
- Before the upload to PyPI nothing is published. Cancel the release run if
  it still waits for approval, fix the problem, delete the tag with
  `git push origin :refs/tags/spec-cleaner-X.Y.Z` (and
  `git tag -d spec-cleaner-X.Y.Z` in any local clone that fetched it), and run
  the tagging workflow again.
- If only the GitHub release failed, re-run the failed job.
- A version on PyPI can never be uploaded again. If it is broken, yank it on
  PyPI and release the next patch version.
