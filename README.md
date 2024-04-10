# HECTRE
### Harvard Extension Clinical Trial Results Extractor
Clinical trial paper data extraction, Harvard Extension collaboration with Pfizer.

## Setup
The tools you'll need are:
- GNU Make (https://www.gnu.org/software/make/) (Additional effort may be needed to install on Windows)
- Python (version >= 3.8)
- AWS credentials to use Amazon Bedrock LLM API (For more information, visit https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html and check under "Long-term credentials", the credentials need to be under your root directory in `.aws` folder, with profile name "[capstone]")

Then, run the following to install all other requirements:
```bash
make setup
```

## Perform Extraction on the Command Line
```bash
make extract path=[FILE OR FOLDER OR URL] picos=[ENDPOINTS SEPARATED BY SEMICOLON]
```

example:
```bash
make extract file=79_Rosenstock_2013.pdf picos=HbA1c
```

Outputs will be saved in `/output/*.csv`.

## Deploy the Web Backend
```bash
make be-dev # run uvicorn with restart
make be-create-items # create items for illustration purposes
make be-get-items # retrieve items for illustration purposes
```
