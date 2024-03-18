# HECTRE Back-End APIs

## Quickstart on Using the APIs

Currently you can just try to invoke the Llama 2 model and see the results.
1. Make sure to have installed Python with at least version 3.8.
2. Make sure AWS credentials are in you root directory under .aws folder.
3. Set the credential profile name to be "capstone".
4. You can run the `local_test.py` with `python -m src.local_test` (or just `python -m local_test` if you are already in the /src directory).
5. Feel free to change `local_test.py` to test out other prompts, or change `config.ini` to change model configurations.

You can also try out doing an extraction on a local PDF file (this will fail for now):
1. Do the setup steps 1-3 from above.
2. Run `local_test_parse_file_path.py` and pass in the PDF file path and the PICOS string as two positional arguments.

## Dev Local Env Notes

The below examples assume your current directory is the repository root, and that you're using an activated Python virtual environment located in PROJECT_ROOT/.venv

Create a virtual environment in the project root and install the requirements
```
# Create the venv
python3 -m venv .venv

# Activate the environment
source .venv/bin/activate

# Install the requirements defined in /requirements.txt
pip install -r src/requirements.txt
```

Install a new package and update requirements.txt
```
# Install the package
pip install pydantic

# Update requirements.txt
pip freeze > src/requirements.txt

# Commit the updated requirements
git add src/requirements.txt && git commit -m "Add pydantic requirement"
```

Select your virtual environment's Python as the VSCode Python interpreter so you can see accurate type hints and warnings, etc in VSCode.
```
# In VSCode, hit Cmd-shift-p and select "Python: Select Interpreter"
# In the dropdown that appears, pick the version of Python located
# in your .venv directory
```
