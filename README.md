# HECTRE
### Harvard Extension Clinical Trial Results Extractor
Clinical trial paper data extraction, Harvard Extension collaboration with Pfizer.

## Setup
The tools you'll need are:
- GNU Make (https://www.gnu.org/software/make/) (Additional effort may be needed to install on Windows)
- Python (version >= 3.9)
- AWS credentials to use Amazon Bedrock LLM API (For more information, visit https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html and check under "Long-term credentials", the credentials need to be under your root directory in `.aws` folder, with profile name "[capstone]")

Then, run the following to install all other requirements:
```bash
make setup
```

## Perform Extraction on the Command Line
```bash
make extract path=[FILE OR FOLDER OR URL] picos=[ENDPOINTS SEPARATED BY SEMICOLON]
```

Simple example:
```bash
make extract file=79_Rosenstock_2013.pdf picos=HbA1c
```

Passing in many different outcomes:
```bash
make extract file=305_deBruin_2018.pdf picos="EASI-50;EASI-75;EASI-90;EASI;SCORAD"
```

Extracting from every PDF in a folder, with the same outcome(s):
```bash
make extract file="folder/pdfs/" picos=HbA1c
```

Extracting from an URL:
```bash
make extract file="https://academic.oup.com/bjd/article-pdf/178/5/1083/47956799/bjd1083.pdf" picos=EASI-75
```

Outputs will be saved in `/output/*.csv`.

## Deploy the Web Backend
```bash
make be-dev # run uvicorn with restart
make be-create-items # create items for illustration purposes
make be-get-items # retrieve items for illustration purposes
```

FastApi will be running on http://127.0.0.1:8000/docs#/

