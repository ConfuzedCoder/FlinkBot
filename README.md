# FlinkBot

pyenv local 3.10.14
poetry init 
poetry shell # Create a virtual env
poetry add ipykernel -G dev

poetry add langchain
poetry add langchain-community
poetry add langchain-cohere 

# Delete virtual enviorment created by poetry
rm -rf {path}

# Creating a virtua env in project folder
export POETRY_VIRTUALENVS_IN_PROJECT=True
poetry shell