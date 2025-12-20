### Python Environment Management with uv
### initialize a project
```bash
uv init --python 3.13
```

```bash
uv run python -V
Python 3.13.11
uv run which python
./.venv/bin/python
```

### add dependencies
```bash
uv add pandas pyarrow
```
we can check the dependecies in /.pyproject.toml




