import Pyro4

def send_pdf_address(pdf_path):
    # Initialize Pyro4 proxy to connect to the MasterServer
    print("Connecting to Master Server...")
    master_server = Pyro4.Proxy("PYRO:master_server@localhost:9090")

    # Send PDF file address to the MasterServer
    master_server.process_pdf(pdf_path)
    print("PDF address sent to Master Server.")

if __name__ == "__main__":
    try:
        print("Connecting to Master Server...")
        # Initialize Pyro4 proxy to connect to the MasterServer
        master_server = Pyro4.Proxy("PYRO:master_server@localhost:9090")
        print("Master Server URI:", master_server._pyroUri)
        
        # Replace 'pdf_path' with the actual path of the PDF file you want to process
        pdf_path = '/Users/shankerltarachandani/Downloads/jemh1dd/jemh1a1.pdf'
        master_server.process_pdf(pdf_path)
        print("PDF address sent to Master Server.")
    except Exception as e:
        print("Error occurred:", e)
