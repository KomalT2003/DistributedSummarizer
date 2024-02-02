import socket

def send_pdf_path_and_receive_text(pdf_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.send(pdf_path.encode('utf-8'))
    
    extracted_text = client_socket.recv(4096).decode('utf-8')
    
    if "Invalid PDF file path." in extracted_text:
        print("Server returned an error: Invalid PDF file path.")
    else:
        print("Extracted Text:")
        print(extracted_text)

    client_socket.close()

pdf_path_to_send = "C:/Users/HP/Downloads/Sample.pdf"
send_pdf_path_and_receive_text(pdf_path_to_send)
