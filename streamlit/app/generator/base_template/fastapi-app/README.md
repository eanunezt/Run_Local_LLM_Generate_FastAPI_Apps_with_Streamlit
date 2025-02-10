configure url db: 
poetry install
poetry run uvicorn src.main:app --reload
