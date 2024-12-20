import PyPDF2

# Open the PDF file in binary read mode
file_object = open("abc.pdf", "rb")

# Initialize the PDF reader
pdf_file_reader = PyPDF2.PdfReader(file_object)

# Variable to store the extracted text
extracted_text = ""

# Loop through the pages and extract text
for page_num in range(len(pdf_file_reader.pages)):
    pdf_page = pdf_file_reader.pages[page_num]  # Access the page correctly
    extracted_text += pdf_page.extract_text()   # Use extract_text() instead of extractText()

# Close the file
file_object.close()

# Print the extracted text
print(extracted_text)