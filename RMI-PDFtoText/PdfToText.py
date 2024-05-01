import PyPDF2
import Pyro4

def pdf_to_text(pdf_path):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        # Initialize Pyro4 proxy to connect to the RMI server
        text_processor = Pyro4.Proxy("PYRO:text_processor@localhost:9090")

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Send page number and text to the RMI server
            text_processor.process_text(page_num + 1, text)

if __name__ == "__main__":
    pdf_path = 'Experiment 04.pdf'
    pdf_to_text(pdf_path)
    print("PDF converted and text sent to server successfully!")