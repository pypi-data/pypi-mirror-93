# Hello World CSTE

This is an example project demonstrating how to publish a python module to PyPI.

## Installation

Run the following to install:

```python
pip install cste-helloworld
```

## Usage

```python
from cstehelloworld import say_hello

# Generate "Hello, World CSTE!"
say_hello()

# Generate "Hello, Antony CSTE!"
say_hello("Antony")
```

## Tests

This is for installing all necesary packeges for testing
```python
pip3 install -e .[dev]
pip install -e .\[dev\]
```
