import json
import os
import re
from jinja2 import Environment, FileSystemLoader

from jinja2_strcase import StrcaseExtension
from utils.str_extension import StrExtension

import shutil


def clean_and_copy_folder(src_path, dest_path):
    """Clean the destination folder and copy the source folder template to it."""
    try:
        # Check if the source folder exists
        if not os.path.exists(src_path):
            raise FileNotFoundError(f"Source folder '{src_path}' does not exist.")

        # Check if the destination folder exists, and remove it if it does
        if os.path.exists(dest_path):
            shutil.rmtree(dest_path)  # Remove the existing folder and its contents
            print(f"Existing folder '{dest_path}' removed.")

        # Create the destination folder
        # os.makedirs(dest_path, exist_ok=True)
        # print(f"Destination folder '{dest_path}' created.")

        # Copy the source folder to the destination
        shutil.copytree(src_path, dest_path)
        print(f"Folder copied successfully from '{src_path}' to '{dest_path}'")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except PermissionError:
        print(f"Error: Permission denied while accessing '{src_path}' or '{dest_path}'")
    except Exception as e3:
        print(f"An error occurred: {e3}")


def clean_generated_folder():    
    src_folder = "./generator/base_template"  # Replace with your source folder path
    dest_folder = "./generator/generated"  # Replace with your destination folder path
    clean_and_copy_folder(src_folder, dest_folder)


clean_generated_folder()


# Define the type mapping function
def map_type(json_type):
    type_mapping = {
        "int": "INTEGER",
        "str": "VARCHAR(255)",
        "text": "TEXT",
        "float": "NUMERIC(12,2)",
        "Any|str": "VARCHAR(255)",
        "Dict": "JSON",
        "bool": "BOOL",
        "UUID": "UUID",
        "date": "date",
        "timestamp": "TIMESTAMP",
    }
    return type_mapping.get(json_type, "TEXT")  # Default to TEXT if type is not found


def sqlalchemy_map_type(json_type: any = str | None):
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


def camel_to_snake(name):
    name = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", name).lower()


def is_nullable(value: any = bool | None) -> str:
    return "True" if value is None else f"{value}"


def create_path(path):
    isExist = os.path.exists(path)
    if not isExist:
        os.makedirs(path)


def create_file(
    env, template_name, model, output_path="./generator/generated/fastapi-app/src"
):
    template = env.get_template(template_name)
    output = template.render(model)
    output_path = f"{output_path}/{model['package'].replace('.', '/')}"
    os.makedirs(output_path, exist_ok=True)
    filename = template_name.replace(".jinja2", "")
    with open(f"{output_path}/{filename}", "w") as f:
        f.write(output)


# Load JSON Data
with open("./generator/models.json", "r") as file:
    models = json.load(file)

# Setup Jinja2 Environment
env = Environment(
    loader=FileSystemLoader("./generator/templates"),
    extensions=[StrcaseExtension, StrExtension],
)
env.globals["map_type"] = map_type  # Register the type mapping function
env.globals["sqlalchemy_map_type"] = (
    sqlalchemy_map_type  # Register the type mapping function
)
env.globals["is_nullable"] = is_nullable


# Generate Code for Each Model
for model in models:
    model["fields"] = [
        {**field, "primary_key": field.get("primary_key", False)}
        for field in model["fields"]
    ]
    model["package"] = model.get("package", "")
    # Generate files
    for template_name in [
        "model.py.jinja2",
        "repository.py.jinja2",
        "service.py.jinja2",
        "controller.py.jinja2",
        "__init__.py.jinja2",
    ]:
        create_file(env=env, template_name=template_name, model=model)


create_file(
    env=env,
    template_name="database.py.jinja2",
    model={"package": ""},
    output_path="./generator/generated/fastapi-app/src",
)
create_file(
    env=env,
    template_name="main.py.jinja2",
    model={"package": "", "models": models},
    output_path="./generator/generated/fastapi-app/src",
)
print("Code generation completed.")
