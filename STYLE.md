# Style

This repo follows **Google** language guides. Agents and students match
them when adding code or comments.

## Python

- Guide: https://google.github.io/styleguide/pyguide.html
- Indent 4 spaces; line length 80; UTF-8
- Docstrings: Google style (module, public functions, public classes)
- Names: `snake_case` functions and variables, `CapWords` classes,
  `UPPER_SNAKE` module constants
- Comments explain *why*, not a restatement of the next line

Ruff is configured in `pyproject.toml` (`pydocstyle` convention
`google`). It is not listed in `requirements.txt`; do not assume it is
installed in `.venv`.

## JavaScript

- Guide: https://google.github.io/styleguide/jsguide.html
- 2-space indent; JSDoc on exported functions

## Docs

- Markdown: short sentences, paths in backticks, no secret values
- Student-facing work lives under `workshop/`
