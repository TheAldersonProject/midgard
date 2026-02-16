# Midgard

Midgard is a Python utility library designed to provide common functionalities shared across different projects. It focuses on simplicity and efficiency, offering tools for logging, file handling, string manipulation, and design patterns.

## Features

- **Logging**: Advanced structured logging powered by `structlog`.
- **File Utilities**: Easy-to-use tools for handling text, JSON, and YAML files, including format conversions, SHA-256 hashing, and Base64 encoding.
- **String Utilities**: Conversions between `CamelCase` and `snake_case`, plus environment variable placeholder replacement in dictionaries.
- **Custom Decorators**: Implementation of common design patterns, such as `@singleton`.

## Requirements

- Python >= 3.13
- Dependencies: `python-dotenv`, `PyYAML`, `structlog`

## Installation

You can install the dependencies using `uv` or `pip`:

```bash
pip install .
```

## Quick Start

### Singleton Decorator
```python
from midgard.custom_decorators import singleton

@singleton
class MyDatabase:
    pass
```

### Logging
```python
from midgard.logs import Logger

logger = Logger.get_logger("my_app")
logger.info("Hello Midgard!")
```

### File Tools
```python
from midgard.file_utils import JsonFileTools

data = JsonFileTools.file_to_json("config.json")
yaml_str = JsonFileTools.json_to_yaml(data)
```

## License

MIT
