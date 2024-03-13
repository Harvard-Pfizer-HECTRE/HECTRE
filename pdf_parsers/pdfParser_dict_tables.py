## pdfParser.py
## Author: Veronika Post
## To run: python pdfParser_dict_tables.py document.pdf
## Dependencies: PyPDF2, tabula

## Description: The script accepts one PDF document as its argument, creates a Python dictionary 
## "paper_dcitionary" where it writes each page under it's number. The indexing starts with 1.
## The script identifies which tables have tables and tries to extract them. The success of extraction
## mostly depends on the format of the paper in the provided PDF file.
## Prints the total number of pages in the PDF file and which of them were identified as containing table/s.

## Note: The page numbers that are in the dictionary start from 0, which is not the same as could be in the PDF.
## The PDF file can have pages from 431 - 437, for example. In the dictionary the page 431 will be page 0.

# necessary imports
import sys
import re
import PyPDF2
from tabula import read_pdf


# dictionary to store the data from the paper
paper_dictionary = {}
# to identify pages with tables
regex_table = r'(^|[\n\w])Table\s+\d+.?\s+\b'
#i = 1


def readPdfFile(filename):
    # try to open a file with the provided name
    try:
        with open(filename, 'rb') as file:
            paper = PyPDF2.PdfFileReader(file)
            # get the number of pages in the PDF
            num_pages = paper.numPages
            print("\nThe document has " + str(num_pages) + " pages.\n")
            i = 1
            for page_number in range(num_pages):
                # create a page object
                pageObj = paper.pages[page_number]
                # extract text from page
                curr_page_text = pageObj.extract_text()
                #print(curr_page_text) # a string object
                # save the page in the dictionary
                paper_dictionary[page_number] = curr_page_text

                # check if the table is present on this page
                if re.search(regex_table, curr_page_text):
                    print("Found table " + str(i) + " on page "+ str(page_number+1) + ".\n")
                    # Some pages can have multiple pages, we have to account for that:
                    # get a list of tables
                    table = read_pdf(filename, pages=page_number+1) # Accepts the page count starting from 1
                    for j in range(0, len(table)):
                        # get rid of indexes
                        table_no_ind = table[j].set_index(table[j].columns[0])
                        #print(table_no_ind.to_string())
                        # save table to dictionary separately
                        paper_dictionary["Table_" + str(i)] = table_no_ind
                        # alternatively if we want to write a string instead of Pandas df
                        #paper_dictionary["Table_" + str(i)] = table_no_ind.to_string()
                        i = i + 1
                        
                else:
                    print("No match.\n")
    
    # if there is no file with this name - throw an error
    except FileNotFoundError:
        print("File not found. Please try again.")

if __name__ == "__main__":
    # if the number of arguments is more or less than one - display usage
    if len(sys.argv) != 2:
        print("Usage: python pdfParser_dict_tables.py <document.pdf>")
    else:
        filename = sys.argv[1]
        readPdfFile(filename)