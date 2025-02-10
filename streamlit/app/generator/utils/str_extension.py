from jinja2.runtime import Undefined
from jinja2.ext import Extension


class StrExtension(Extension):
    """
    Custom Jinja2 extension to transform strings into different cases.
    """

    # The list of Jinja2 tags this extension supports (not required for simple filters)
    tags = set()

    def __init__(self, environment):
        super().__init__(environment)

        # Register custom filters
        environment.filters["upper"] = self.upper
        environment.filters["lower"] = self.lower
        environment.filters["title"] = self.title
        environment.filters["is_required"] = self.is_required
        environment.filters["is_nullable"] = self.is_nullable
        environment.filters["get_package"] = self.get_package
        environment.filters["sqlalchemy_type"] = self.sqlalchemy_type

    def upper(self, value):
        """Convert string to uppercase."""
        return value.upper() if isinstance(value, str) else value

    def lower(self, value):
        """Convert string to lowercase."""
        return value.lower() if isinstance(value, str) else value

    def title(self, value):
        """Convert string to title case."""
        return value.title() if isinstance(value, str) else value

    def is_required(self, value):
        if isinstance(value, Undefined):
            return False
        return value

    def is_nullable(self, value):
        if value:
            return value
        else:
            return True
        
    def get_package(self, value):
        return value.get("package", "")

    def sqlalchemy_type(self, json_type: any = str | None):
        type_mapping = {
            "int": "Integer",
            "str": "String(255)",
            "text": "Text",
            "float": "Float(precision=12)",
            "Any|str": " String(255)",
            "Dict": "JSON",
            "bool": "Boolean",
            "UUID": "UUID(as_uuid=True)",
            "date": "Date",
            "timestamp": "DateTime",
        }
        return type_mapping.get(json_type, "Text")
