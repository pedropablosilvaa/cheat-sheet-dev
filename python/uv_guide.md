# **uv Cheat Sheet**

## **What is uv?**

- **uv** is a fast Python package installer and resolver written in Rust.
- It replaces `pip`, `pip-tools`, and even `pyenv` for managing Python installations.
- Key features:
  - **Speed**: Up to 100x faster than `pip`.
  - **Disk efficiency**: Uses a global cache to avoid duplicate package installations.
  - **Cross-platform**: Works on macOS, Linux, and Windows.
  - **Virtual environment management**: Simplifies creating and syncing virtual environments.

---

## **Installation**

1. **Install uv**:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

2. **Verify installation**:

   ```bash
   uv --version
   ```
  
## Managing Python Versions

- Install the latest version:

  ```bash
  uv python install
  ```

- To install a specific Python version:

  ```bash
  uv python install 3.12.6
  ```

- List installed Python versions:

  ```bash
  uv python list
  ```

- Set a default Python version:
  
  ```bash
  uv python default 3.12.6
  ```

## Project setup

1. Initialize a new project and creates a pyproject.toml file and a src/ directory:

    ```bash
    uv init
    ```

2. Creates a .venv folder in the project directory:

    ```bash
    uv venv
    ```


- To specify a custom name or Python version:

    ```bash
    uv venv my-env --python 3.12.4
    ```

3. Activate the virtual environment:

    ```bash
    source .venv/bin/activate
    ```

## Dependency Managment

Add a package:

```bash
uv add pandas
```

Install dependencies from pyproject.toml:

```bash
uv sync
```

Generate a requirements.txt file:

```bash
uv pip freeze > requirements.txt
```

Install from requirements.txt:

```bash
uv pip install -r requirements.txt
```

Remove a package:

```bash
uv remove pandas
```

## Syncing Environments

Sync the virtual environment with pyproject.toml:

```bash
uv sync
```

- Installs missing packages.

- Upgrades/downgrades packages to match versions in pyproject.toml.

- Removes unused packages.

To find the path of the current active env:

```bash
uv python find
```
