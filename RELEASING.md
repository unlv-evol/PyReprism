# Releasing PyReprism

Releases are automated: **pushing a `vX.Y.Z` tag** builds the package, publishes it
to PyPI, and creates a GitHub Release. You never edit the version in more than one
place — `src/PyReprism/__init__.py` is the single source of truth and
`pyproject.toml` derives the version from it.

## One-time setup (Trusted Publishing)

Publishing uses PyPI [Trusted Publishing](https://docs.pypi.org/trusted-publishers/)
(OIDC) — no API token. Configure it once:

1. **PyPI** → the `PyReprism` project → *Publishing* → add a GitHub publisher:
   - Repository: `unlv-evol/PyReprism`
   - Workflow: `publish.yml`
   - Environment: `pypi`
2. **GitHub** → repo *Settings → Environments* → create an environment named
   `pypi` (optionally require a reviewer to approve each release).

## Cutting a release

1. **Bump the version** in [`src/PyReprism/__init__.py`](src/PyReprism/__init__.py):

   ```python
   __version__ = "0.2.0"
   ```

2. **Update the changelog** in [`CHANGELOG.md`](CHANGELOG.md): rename the
   `## [Unreleased]` heading to `## [0.2.0] - YYYY-MM-DD`, add a fresh empty
   `## [Unreleased]` above it, and update the link references at the bottom.

3. **Commit, tag, and push** (the tag must equal the version — CI verifies it):

   ```shell
   git commit -am "release: v0.2.0"
   git tag -a v0.2.0 -m "v0.2.0"
   git push origin main --follow-tags
   ```

That's it. Pushing the tag triggers [`publish.yml`](.github/workflows/publish.yml),
which:

1. checks that the tag matches `__version__`,
2. builds the sdist + wheel and runs `twine check`,
3. publishes to PyPI via Trusted Publishing, and
4. creates a GitHub Release titled `v0.2.0` with notes taken from the matching
   `CHANGELOG.md` section and the built artifacts attached.

## Versioning

PyReprism follows [Semantic Versioning](https://semver.org): bump **patch** for
fixes, **minor** for backwards-compatible features, **major** for breaking changes.

## Testing a release without publishing

To validate the build locally before tagging:

```shell
python -m build
twine check dist/*
```
