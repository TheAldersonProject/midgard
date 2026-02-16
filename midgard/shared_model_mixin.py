"""Shared Model Mixin."""

from glom import glom
from jinja2 import Template
from tabulate import tabulate


class SharedModelMixin:
    """Shared Model Mixin."""

    @property
    def content_report(self) -> str:
        """Build a content report in Markdown format."""

        def sanitize_for_markdown_table(data_list):
            sanitized_list = []
            for row in data_list:
                new_row = {}
                for key, value in row.items():
                    v_ = str(value)
                    v_ = v_.replace("\n", " ").replace("<br>", " ").strip()
                    new_row[key] = v_
                sanitized_list.append(new_row)
            return sanitized_list

        template_ = """# Document: {{ title }} - {{ description }}\n### Attributes:\n"""
        model_as_json = self.model_json_schema()
        model_instance_as_dict = self.model_dump()

        values_ = {
            "title": glom(model_as_json, "title", default="No title available"),
            "description": glom(model_as_json, "description", default="No description available."),
        }
        if "properties" in model_as_json:
            for key, value in model_as_json["properties"].items():
                if "$ref" in value:
                    value = model_as_json["$defs"][value["$ref"].split("/")[-1]]

                data_type = value["type"] if "type" in value else "string"
                instance_value = glom(model_instance_as_dict, f"{key}", default={})

                if not instance_value:
                    continue

                if isinstance(instance_value, list):
                    if isinstance(instance_value[0], dict):
                        instance_value = tabulate(
                            sanitize_for_markdown_table(instance_value),
                            headers="keys",
                            tablefmt="github",
                        )

                    else:
                        instance_value = [f"    - {i}" for i in instance_value]
                        instance_value = "\n".join(instance_value)
                        instance_value = "\n" + instance_value

                elif isinstance(instance_value, dict):
                    formatted_value = "\n"
                    lov = []
                    for k, v in instance_value.items():
                        formatted_value += f"   - **`{k}`**: `{v}`\n"
                        lov.append(formatted_value)

                    instance_value = "".join(lov)

                elif data_type == "string" and value.get("format", "") == "date-time":
                    if isinstance(instance_value, str):
                        from dateutil.parser import parse

                        instance_value = parse(instance_value)

                    instance_value = instance_value.strftime("%Y-%m-%d %H:%M:%S")

                title_ = value["title"] if "title" in value else key.capitalize()
                template_ += f"#### **{title_}:**\n {instance_value}\n"

            template = Template(template_)
            rendered = template.render(**values_)

            return rendered

        return ""
