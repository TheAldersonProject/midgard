"""
Provides utility methods for file handling and JSON/YAML processing.

This module is intended to offer various tools for working with text files,
JSON files, YAML files, and data serialization. It includes functionality to
read/write file content, convert between JSON and YAML formats, generate hashes,
and encode data. All methods are static and can be used without instantiating
classes, making them light and convenient for utilities.
"""

import base64
import hashlib
import json
from pathlib import Path

import yaml


class FileTools:
    """
    Provides static utility methods for file handling operations.

    This class is designed to perform common file-related tasks,
    such as reading the content of a file. All methods are static
    for ease of use and do not require instantiation of the class.
    """

    @staticmethod
    def read_text_content(file_path: str) -> str:
        """
        Reads the text content from a specified file.

        Opens the file located at the given file path, reads its content, and returns it
        as a string. This method assumes the file contains plain text and will read the
        entirety of the file into memory.

        :param file_path: The path to the file to be read.
        :type file_path: str
        :return: The text content of the specified file.
        :rtype: str
        """

        with open(file_path, "r") as file:
            return file.read()


class JsonFileTools:
    """JSON & YAML file tools."""

    @staticmethod
    def file_to_json(file_path: str) -> dict:
        """
        Converts the content of a JSON file into a Python dictionary.

        This method reads the provided JSON file from the given file path, parses
        its content, and returns it as a Python dictionary. If the file is empty or
        its content is invalid, an empty dictionary is returned.

        :param file_path: The path to the JSON file to be read.
        :type file_path: str
        :return: A dictionary representing the JSON file content.
        :rtype: dict
        """

        with open(file_path, "r") as f:
            schema_content = json.load(f)

        return schema_content or {}

    @staticmethod
    def json_to_yaml(json_content: dict) -> str:
        """
        Converts a JSON content dictionary into a formatted YAML string.

        This static method takes in a dictionary representing JSON content, converts
        it into a YAML string, and formats the output with specific configuration
        for readability. The output YAML string maintains input ordering, disables
        the default flow style, and applies a consistent indentation of 4 spaces.

        :param json_content: The dictionary containing JSON content to be converted.
        :type json_content: dict
        :return: A YAML formatted string generated from the JSON content.
        :rtype: str
        """
        return yaml.dump(json.loads(json_content), sort_keys=False, default_flow_style=False, indent=4)

    @staticmethod
    def yaml_to_json(file_path: str) -> dict:
        """
        Converts a YAML file to a JSON-compatible Python dictionary.

        This static method reads the contents of a YAML file specified by the file path
        and converts it into a dictionary that is JSON-compatible. It utilizes the
        `yaml.safe_load` function to parse the YAML content while maintaining safety
        against arbitrary code execution. This method is particularly useful for
        extracting structured data stored in YAML format for JSON processing or storage.

        :param file_path: The path to the YAML file to be converted.
        :type file_path: str
        :return: A dictionary representing the contents of the YAML file, structured
                 in a way that is JSON-compatible.
        :rtype: dict
        """

        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def json_to_yaml_file(file_path: str, content: dict) -> None:
        """
        Converts a JSON-compatible dictionary into a YAML file and saves it to the specified file path.

        :param file_path: The path to the YAML file where the content will be saved.
        :param content: The dictionary containing data to be converted and saved as YAML.
        :return: None
        """

        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    @staticmethod
    def json_to_sha256(data: dict) -> str:
        """
        Converts a given JSON-serializable dictionary into a SHA-256 hash. The input
        dictionary is serialized into a canonical JSON string format with keys sorted
        and no unnecessary whitespace. The resulting string is then used to compute
        a SHA-256 hash. This utility is commonly used in applications requiring
        consistent and reproducible hash generation from JSON-like data.

        :param data: A dictionary to be serialized into JSON and hashed. It should
            be JSON-serializable and not contain unserializable objects such as
            functions or complex custom classes.
        :type data: dict
        :return: The SHA-256 hash of the canonical JSON string representation of the
            input dictionary.
        :rtype: str
        """

        algorithm: str = "sha256"
        canonical_json = json.dumps(data, sort_keys=True, indent=None, separators=(",", ":"))
        hasher = hashlib.new(algorithm)
        hasher.update(canonical_json.encode("utf-8"))

        return hasher.hexdigest()

    @staticmethod
    def json_to_base64(content: dict) -> str:
        """
        Encodes a given JSON-serializable dictionary into a Base64 encoded string.

        This static method takes a dictionary, serializes it into a JSON string,
        and then encodes the JSON string into a Base64-encoded format. The result
        is a `str` that represents the Base64 encoding of the input dictionary.

        :param content:
            The dictionary to be converted to a Base64 encoded string. Must be
            a valid JSON-serializable object.
        :return:
            A Base64-encoded string representation of the input dictionary.
        """

        return base64.b64encode(json.dumps(content).encode("utf-8")).decode("utf-8")
