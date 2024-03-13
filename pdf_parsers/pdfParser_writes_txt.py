## pdfParser.py
## Author: Veronika Post
## To run: python pdfParser.py document.pdf
## Dependencies: PyPDF2

## Description: The script accepts one PDF document as its argument, writes the text and tables from that
## PDF document into the file with the same name + "_output.txt". The output is broken down in pages as theay
## appear in the PDF.

## Note: Not always the page number that is being printed out here is the same as the page number in the text.
## That could be fixed if it's a good idea.

# necessary imports
import sys
import os
import PyPDF2


def generateOutputFile(pdf_filename):
    # Get the input filename without an extension
    filename_no_extension = os.path.splitext(pdf_filename)[0]
    return filename_no_extension + "_output.txt"

def readPdfFile(filename):
    # try to open a file with the provided name
    try:
        outputFile = generateOutputFile(filename)
        with open(filename, 'rb') as file, open(outputFile, 'w') as output:
            paper = PyPDF2.PdfFileReader(file)
            # get the number of pages in the PDF
            num_pages = paper.numPages
            print("\nThe document has " + str(num_pages) + " pages.\n")
            output.write("\nThe document has " + str(num_pages) + " pages.\n")
            for page_number in range(num_pages):
                # create a page object
                pageObj = paper.pages[page_number]
                print("\n\n-------Below is the text content of " + filename + " on page " + str(page_number+1) + ":----------\n\n")
                output.write("\n\n-------Below is the text content of " + filename + " on page " + str(page_number+1) + ":----------\n\n")
                # extract text from page
                print(pageObj.extract_text())
                output.write(pageObj.extract_text())
    
    # if there is no file with this name - throw an error
    except FileNotFoundError:
        print("File not found. Please try again.")

if __name__ == "__main__":
    # if the number of arguments is more or less than one - display usage
    if len(sys.argv) != 2:
        print("Usage: python pdfParser.py <document.pdf>")
    else:
        filename = sys.argv[1]
        readPdfFile(filename)