"""
Module for string manipulation utilities.

This module provides a utility class `StringUtils` with static methods for commonly
used string transformations, such as conversions between CamelCase and snake_case
formats, and replacement of placeholders in dictionaries with environment variable
values. The module has optional support for `.env` files via the `python-dotenv`
package.
"""

import os
import re
from typing import Any

from dotenv import load_dotenv


class StringUtils:
    """
    Utility class for string manipulation.

    This class provides methods to perform common string transformations, such as conversion
    between CamelCase and snake_case formats, as well as replacing placeholders in dictionaries
    with corresponding environment variable values.

    The methods of this class are implemented as static methods, allowing their usage without
    the need to instantiate the class.
    """

    @staticmethod
    def camel_to_snake(value: str) -> str:
        """
        Converts a string from CamelCase to snake_case.

        This method processes a given CamelCase formatted string and transforms it into
        a snake_case formatted string. It uses regular expressions to identify and
        properly separate words based on uppercase letters and numbers.

        :param value: The CamelCase formatted string to convert.
        :type value: str
        :return: The converted snake_case formatted string.
        :rtype: str
        """

        value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
        value = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", value)

        return value.lower()

    @staticmethod
    def snake_to_camel(value: str) -> str:
        """
        Converts a snake_case string to camelCase.

        This method takes a string formatted in snake_case and converts it into
        camelCase. It uses regular expressions to identify and transform the
        patterns accordingly.

        :param value: A string in snake_case format.
        :type value: str
        :return: A string transformed into camelCase format.
        :rtype: str
        """

        value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1_\2", value)
        value = re.sub(r"([a-z\d])([A-Z])", r"\1_\2", value)

        return value.lower()

    @staticmethod
    def replace_placeholders_with_env_values(value: Any, load_dot_env: bool = False) -> dict[str, str | Any]:
        """
        Replace placeholders in a given dictionary with corresponding environment variable
        values. Supports optional dotenv file loading and default values for placeholders
        in the form `${VAR_NAME:-default_value}`.

        :param value: A dictionary containing string placeholders in the form `${VAR_NAME}`
            or `${VAR_NAME:-default_value}`. Nested dictionaries are supported.
        :type value: dict[str, str | dict]
        :param load_dot_env: A boolean flag to determine whether to load environment
            variables from a `.env` file in the working directory before substitution. If it
            is set to True, the `load_dotenv` function is called.
        :type load_dot_env: bool

        :return: The input dictionary with placeholders replaced by the corresponding
            environment variable values or default values when applicable.
        :rtype: dict[str, str | Any]
        """

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
