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