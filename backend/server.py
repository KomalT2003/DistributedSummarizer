import socket
import os
import fitz  # PyMuPDF

def extract_text_from_pdf(pdf_path):
    pdf_document = fitz.open(pdf_path)
    text_content = ""
    for page_number in range(pdf_document.page_count):
        page = pdf_document[page_number]
        text_content += page.get_text()
    pdf_document.close()
    return text_content

def handle_client(client_socket):
    pdf_path = client_socket.recv(1024).decode('utf-8')

    if not os.path.isfile(pdf_path):
        client_socket.send(b"Invalid PDF file path.")
        return
    extracted_text = extract_text_from_pdf(pdf_path)

    client_socket.send(extracted_text.encode('utf-8'))

    client_socket.close()

def start_server():
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 5555))

    server_socket.listen(5)
    print("Server listening on port 5555...")

    while True:
        
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")
        handle_client(client_socket)

if __name__ == "__main__":
    start_server()
