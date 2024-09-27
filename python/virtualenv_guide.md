
# Python Virtualenv Guide

This guide provides the primary commands to utilize Python's `virtualenv` across various operating systems including Windows, Ubuntu (Linux), and macOS.

## Installation

First, ensure that Python and pip are installed on your system. Then, install `virtualenv` using pip:

```bash
pip install virtualenv
```

## Usage

### Creating a Virtual Environment

- **Windows**
  ```cmd
  python -m virtualenv venv
  ```

- **Ubuntu / macOS**
  ```bash
  python3 -m virtualenv venv
  ```

### Activating the Virtual Environment

- **Windows**
  ```cmd
  .\venv\Scripts\activate
  ```

- **Ubuntu / macOS**
  ```bash
  source venv/bin/activate
  ```

### Deactivating the Virtual Environment

Regardless of the operating system, you can deactivate the virtual environment with:

```bash
deactivate
```

## Requirements File

To keep track of your dependencies, you can create a `requirements.txt` file by running:

```bash
pip freeze > requirements.txt
```

And to install all dependencies listed in the file:

```bash
pip install -r requirements.txt
```

## Restart env
- Reiniciar env
  ´´´bash
  deactivate
  rm -rf venv
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.txt
  ´´´


---
