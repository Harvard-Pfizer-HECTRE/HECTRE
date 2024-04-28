# HECTRE
### Harvard Extension Clinical Trial Results Extractor
Clinical trial paper data extraction, Harvard Extension collaboration with Pfizer.
This tool will assist in meta-analysis by extracting clinical data from clinical trial paper PDFs in a specific format that is usable for Pfizer.

**This is the technical setup and configuration guide for deployment. For [user guide after setup, click here.](/USER_GUIDE.md)**

## Setup
The tools you'll need are:
- (For Windows) GNU Make (https://www.gnu.org/software/make/)
- Python (version >= 3.9)
- AWS credentials to use Amazon Bedrock LLM API (For more information, visit https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-files.html and check under "Long-term credentials", the credentials need to be under your root directory in `.aws` folder)

Then, run the following to setup and install requirements if deploying on current system:
```bash
make setup
```

Or, running in a virtual environment:
```bash
make vsetup
```

## Configurations
Please see [config.yaml file.](/config.yaml)
You can change many fields, such as the PDF parser used, the LLM used, LLM parameters, and logging verbosity.

## Make Changes to Prompting Methodology
Also in the [config.yaml file.](/config.yaml)
The text for each prompt used is in this file, and you may edit it as you see fit. You can also add multi-shot prompting. Example:
Current prompt:
```
  PromptTableOnPage1: |-
    Below is a page from a clinical trial paper parsed from PDF:
    {Text_Start_Indicator}{Text}{Text_End_Indicator}
    If there are any number of tables with clinical data on this page, answer exactly with "YES"; otherwise answer exactly with "NO".
```
Possible change:
```
  PromptTableOnPage1: |-
    Below is a page from a clinical trial paper parsed from PDF:
    {Text_Start_Indicator}{Text}{Text_End_Indicator}
    Does this page have any tables?
  PromptTableOnPage2: |-
    Are you sure the answer is correct? Tell me about the columns and rows of any tables on this page, and what clinical data can be derived from them.
  PromptTableOnPage3: |-
    Ok, now respond with "YES" or "NO" regarding if there is any tables with actual clinical data on this page.
```

## Make Changes to Field Definitions
Each column has a specific name and description used as explanation to the LLM performing the extraction. Editing them may improve extraction results. As an example, you may change the field description of `STATANAL.IMP.METHOD` to say select from a small given pool of choices, or say to derive it straight from the paper.
Currently, only the fields `Field Label` and `Field Description` are used, so you only have to edit those.
[Click here to see the current field definitions.](/hectre/definitions.json)

## Deploy the Web Backend
```bash
make be-dev # run uvicorn with restart
make be-create-items # create items for illustration purposes
make be-get-items # retrieve items for illustration purposes
```

FastApi will be running on http://127.0.0.1:8000/docs#/

