import Pyro4
import PyPDF2

# Import the TextProcessorServer class from your TextServer file
from TextServer import TextProcessorServer

@Pyro4.expose
class MasterServer:
    def __init__(self):
        print("Master Server initialized.")
        pass

    def process_pdf(self, pdf_path):
        # Initialize Pyro4 proxy to connect to the TextProcessorServer
        text_processor = Pyro4.Proxy("PYRO:text_processor@localhost:9091")
        
        # Call pdf_to_text function from your PDFToText file
        pdf_to_text(pdf_path, text_processor)

def pdf_to_text(pdf_path, text_processor):
    # Open the PDF file in read-binary mode
    with open(pdf_path, 'rb') as pdf_file:
        # Create a PdfReader object instead of PdfFileReader
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()
            # Send page number and text to the TextProcessorServer
            text_processor.process_text(page_num + 1, text)

if __name__ == "__main__":
    try:
        print("Attempting to register MasterServer...")
        # Register the MasterServer with Pyro4
        daemon = Pyro4.Daemon()
        ns = Pyro4.locateNS()
        uri = daemon.register(MasterServer)
        ns.register("master_server", uri)

        print("Master Server registered successfully.")
        print("Master Server URI:", uri)
        print("Master Server is ready.")
        daemon.requestLoop()
    except Exception as e:
        print("Error occurred:", e)

