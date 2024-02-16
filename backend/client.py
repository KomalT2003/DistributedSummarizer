import socket
from count import process_text_in_chunks
def send_pdf_path_and_receive_text(pdf_path):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 5555))
    client_socket.send(pdf_path.encode('utf-8'))
    
    extracted_text = client_socket.recv(4096).decode('utf-8')
    
    if "Invalid PDF file path." in extracted_text:
        print("Server returned an error: Invalid PDF file path.")
    else:
        print("00:00:00")
        process_text_in_chunks(extracted_text, 5)
        print("00:00:14")
        total_count=0
        extracted_text=extracted_text.split(" ")
        print("_________________________________________________")
        
        print("\nWithout threadfing")
        for i in range(0,100000):
            for j in range(0,200):
                continue
        
        for i in extracted_text:
            if i=="the":
                total_count+=1
        print("Number of \"the\" :", total_count)
        print("00:02:09")

    client_socket.close()

pdf_path = "C:/Users/HP/Downloads/Sample_Input.pdf"
send_pdf_path_and_receive_text(pdf_path)
