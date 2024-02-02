import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_content = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text_content += page.get_text()
    pdf_document.close()
    return text_content

# Example usage
pdf_path = "C:/Users/HP/Downloads/Sample.pdf"
extracted_text = extract_text_from_pdf(pdf_path)

# Print or use the extracted text as needed
print(extracted_text)
