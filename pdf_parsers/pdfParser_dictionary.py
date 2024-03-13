## pdfParser.py
## Author: Veronika Post
## To run: python pdfParser_dictionary.py document.pdf
## Dependencies: PyPDF2

## Description: The script accepts one PDF document as its argument, creates a Python dictionary 
## "paper_dcitionary" where it writes each page under it's number. The indexing starts with 1.
## Prints the total number of pages in the PDF file.

## Note: The page numbers that are in the dictionary start from 0, which is not the same as could be in the PDF.
## The PDF file can have pages from 431 - 437, for example. In the dictionary the page 431 will be page 0.

# necessary imports
import sys
import os
import PyPDF2


# dictionary to store the data from the paper
paper_dictionary = {}


def readPdfFile(filename):
    # try to open a file with the provided name
    try:
        with open(filename, 'rb') as file:
            paper = PyPDF2.PdfFileReader(file)
            # get the number of pages in the PDF
            num_pages = paper.numPages
            print("\nThe document has " + str(num_pages) + " pages.\n")
            for page_number in range(num_pages):
                # create a page object
                pageObj = paper.pages[page_number]
                # extract text from page
                # uncomment the following line to see the value of each key
                #print(pageObj.extract_text())
                # save the page in the dictionary
                paper_dictionary[page_number] = pageObj.extract_text()
    
    # if there is no file with this name - throw an error
    except FileNotFoundError:
        print("File not found. Please try again.")

if __name__ == "__main__":
    # if the number of arguments is more or less than one - display usage
    if len(sys.argv) != 2:
        print("Usage: python pdfParser_dictionary.py <document.pdf>")
    else:
        filename = sys.argv[1]
        readPdfFile(filename)