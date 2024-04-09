# HECTRE Back-End APIs

## Quickstart on Using the APIs

You can provide a local path of a PDF or URL to a PDF, as well as endpoints separated by semi-colon, to the `/src/extract_single_file.py` script to perform data extraction. Output will be in `/output/<date and time>.csv`.
1. Make sure to have installed Python with at least version 3.8.
2. Make sure AWS credentials are in you root directory under .aws folder. (For more information, visit https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html and check under "Long-term credentials")
3. Set the credential profile name to be "capstone". (ex: typically there is `[default]` or `[user1]`, set the AWS credentials to be `[capstone]`)
4. You can run the `/src/extract_single_file.py` with `python -m src.extract_single_file <path or URL> <endpoints separated by semi-colon>`.

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
