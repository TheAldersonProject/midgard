"""Set of file utilities."""
import base64
import hashlib
import json
from pathlib import Path

import yaml


class GeneralFileTools:
    """General file tools."""

    @staticmethod
    def get_file_string_content(file_path: str) -> str:
        """Get file content as a string."""

        with open(file_path, "r") as file:
            return file.read()


class JsonFileTools:
    """JSON & YAML file tools."""

    @staticmethod
    def file_to_json(file_path: str) -> dict:
        """Get file content as JSON."""

        with open(file_path, "r") as f:
            schema_content = json.load(f)

        return schema_content or {}

    @staticmethod
    def json_to_yaml(json_content: dict) -> str:
        """Converts a JSON content to YAML format."""
        return yaml.dump(json.loads(json_content), sort_keys=False, default_flow_style=False, indent=4)

    @staticmethod
    def yaml_to_json(file_path: str) -> dict:
        """Loads a YAML file and returns its content as a dictionary."""

        with open(file_path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def json_to_yaml_file(file_path: str, content: dict) -> None:
        """Save YAML content to a file."""

        file_path = Path(file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)

    @staticmethod
    def json_to_sha256(data: dict) -> str:
        """Generates a sha256 signature for a JSON object."""

        algorithm: str = "sha256"
        canonical_json = json.dumps(data, sort_keys=True, indent=None, separators=(",", ":"))
        hasher = hashlib.new(algorithm)
        hasher.update(canonical_json.encode("utf-8"))

        return hasher.hexdigest()

    @staticmethod
    def json_to_base64(content: dict) -> str:
        """Pack JSON content as base64."""

        return base64.b64encode(json.dumps(content).encode("utf-8")).decode("utf-8")
