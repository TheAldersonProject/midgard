"""String utilities."""

import os
import re
from typing import Any

from dotenv import load_dotenv


class StringUtils:
    """String utilities."""

    @staticmethod
    def camel_to_snake(value: str) -> str:
        """Converts a camelCase string to a snake_case string."""

        value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
        value = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", value)

        return value.lower()

    @staticmethod
    def snake_to_camel(value: str) -> str:
        """Converts a snake_case string to a camelCase string."""

        value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
        value = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", value)

        return value.lower()

    @staticmethod
    def replace_placeholders_with_env_values(value: Any, load_dot_env: bool = False) -> dict[str, str | Any]:
        """Replace placeholders with environment variables."""

        if load_dot_env:
            load_dotenv()

        pattern = re.compile(r"\$\{([^}]+)\}")

        def replace_match(match):
            """Replace a match with the corresponding environment variable value."""
            var = match.group(1)
            if ":-" in var:
                var_name, default = var.split(":-", 1)
            else:
                var_name, default = var, None

            return os.getenv(var_name, default)

        def replace_dict(d) -> None:
            """Recursively replace placeholders in a dictionary."""
            for key, value in d.items():
                if isinstance(value, dict):
                    replace_dict(value)
                elif isinstance(value, str):
                    d[key] = pattern.sub(replace_match, value)

        replace_dict(value)

        return value
