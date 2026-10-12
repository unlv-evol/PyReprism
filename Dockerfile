# PyReprism CLI, containerized.
#
#   docker build -t pyreprism .
#   docker run --rm -v "$PWD:/work" pyreprism clones . --reporter sarif
#   docker run --rm -v "$PWD:/work" pyreprism scan . --json
#
# The image ships the 187-language, zero-dependency lexical core plus the
# optional Pygments backend ([accurate], pure Python). The heavier [ast]
# (tree-sitter) and [semantic] (torch/transformers) tiers are intentionally
# left out to keep the image small; derive your own image if you need them.

# ---- build stage: produce a wheel from the source tree ----
FROM python:3.12-slim AS build
WORKDIR /src
# Only the files hatchling needs to build the wheel and read metadata.
COPY pyproject.toml LICENSE ./
COPY docs/intro.rst ./docs/intro.rst
COPY src ./src
RUN pip install --no-cache-dir build \
    && python -m build --wheel --outdir /dist

# ---- runtime stage: install the wheel, drop the build tooling ----
FROM python:3.12-slim
LABEL org.opencontainers.image.title="PyReprism" \
      org.opencontainers.image.description="Lossless token substrate for polyglot code analysis (CLI)" \
      org.opencontainers.image.source="https://github.com/unlv-evol/PyReprism" \
      org.opencontainers.image.licenses="MIT"
COPY --from=build /dist/*.whl /tmp/
RUN pip install --no-cache-dir "$(ls /tmp/*.whl)[accurate]" \
    && rm -rf /tmp/*.whl /root/.cache/pip
# Run as an unprivileged user; /work is where the caller mounts their code.
RUN useradd --create-home --uid 1000 app
USER app
WORKDIR /work
ENTRYPOINT ["pyreprism"]
CMD ["--help"]
