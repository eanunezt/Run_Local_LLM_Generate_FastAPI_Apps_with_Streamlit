import os
import json
import shutil
import subprocess
import streamlit as st
from pathlib import Path
from langchain.chains import LLMChain
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate
from text_templates import DSL_JSON_TEMPLATE

# Define paths
#CURREN_DIR = os.getcwd()
MODEL_JSON_PATH = Path("./generator/models.json")
GENERATOR_SCRIPT = Path("./generator/generate_code.py")
GENERATOR_BASE_PATH = "./generator/generated"
GENERATED_FOLDER = Path(f"{GENERATOR_BASE_PATH}/fastapi-app")
ZIP_FILE_PATH = Path(f"{GENERATOR_BASE_PATH}/fastapi-app.zip")


def load_llm():
    """Load the LLM model from Ollama."""
    return OllamaLLM(
        model=os.getenv("MODEL_LLM", "mistral"),
        base_url=os.getenv("BASE_URL_SRV_LLM", "http://localhost:11434"),
    )


# Initialize LLM model
llm = load_llm()

# Define prompt template for SQL to JSON conversion
prompt = PromptTemplate(
    input_variables=["ddl_sql", "dsl_json_template"],
    template=(
        "Convert the following SQL DDL statement into a valid JSON format. "
        "Ensure the output is strictly JSON without extra text. Do not include any explanations or preamble:\n\n"
        "{ddl_sql}\n\n"
        "Please note the following JSON DSL:\n\n"
        "{dsl_json_template}\n\n"
        "Respond only with a valid JSON object."
    ),
)

chain = LLMChain(llm=llm, prompt=prompt)


def convert_sql_to_json(ddl_sql):
    """Use LLM to convert SQL to JSON and write it to model.json."""
    response = chain.invoke(
        {"ddl_sql": ddl_sql, "dsl_json_template": DSL_JSON_TEMPLATE}
    )

    if not response:
        st.error("No response from the model.")
        return None

    try:
        json_output = json.loads(response.get("text", "{}"))
        with open(MODEL_JSON_PATH, "w") as json_file:
            json.dump(json_output, json_file, indent=4)
        st.success("JSON generared:")
        return json_output
    except json.JSONDecodeError:
        st.error(
            "Failed to parse JSON response. The model may have returned invalid JSON."
        )
        return None


def generate_project():
    """Run the generate_code.py script to create a project template."""
    if GENERATOR_SCRIPT.exists():
        try:
            subprocess.run(["python", str(GENERATOR_SCRIPT)], check=True)
            # st.success("Project template generated successfully.")
        except subprocess.CalledProcessError as e:
            st.error(f"Error generating project: {e}")
    else:
        st.error(f"Generator script not found: {GENERATOR_SCRIPT}")


def create_zip():
    """Create a ZIP file from the generated project folder."""
    if GENERATED_FOLDER.exists():
        shutil.make_archive(
            str(ZIP_FILE_PATH).replace(".zip", ""), "zip", GENERATED_FOLDER
        )
        st.success("ZIP file created successfully.")
    else:
        st.error(f"Generated folder not found: {GENERATED_FOLDER}")


def main():
    st.title("DDL SQL to JSON & Code Generator")

    # Step 1: Convert SQL to JSON and save
    ddl_sql = st.text_area("Enter your DDL SQL statement:", height=200)
    if st.button("Generate Project"):
        if ddl_sql.strip():
            json_output = convert_sql_to_json(ddl_sql)
            if json_output:
                st.json(json_output)
                generate_project()
                create_zip()
        else:
            st.warning("Please enter a valid SQL DDL statement.")

    # Step 4: Provide download button if ZIP exists
    if ZIP_FILE_PATH.exists():
        with open(ZIP_FILE_PATH, "rb") as f:
            st.download_button(
                label="Download Project ZIP",
                data=f,
                file_name="fastapi-app.zip",
                mime="application/zip",
            )
    if os.path.exists(GENERATOR_BASE_PATH):
        shutil.rmtree(GENERATOR_BASE_PATH)  
        print(f"Existing folder '{GENERATOR_BASE_PATH}' removed.")


if __name__ == "__main__":
    main()
