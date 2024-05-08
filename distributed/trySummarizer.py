import requests
import PyPDF2
from transformers import BartForConditionalGeneration, BartTokenizer
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from flask import Flask, request, jsonify
app=Flask(__name__)

@app.route("/",methods=["GET"])
def home():
    return "Hello, World!"




@app.route("/upload", methods=["GET"])
def upload():
        # print("File received")
        # file = "PlacesInIndia.pdf"
        # print("File name: ", file.filename)
        # file.save(file.filename)
        # print("File uploaded successfully")
        # summaries_list = summarize_all_pages(file.filename)
        # create_summary_pdf(summaries_list)
        # return "File uploaded successfully"
        pdf_path = "/Users/shankerltarachandani/Downloads/PlacesInIndia.pdf"
        print("Started summarization")
        
        summary_text = summarize_all_pages(pdf_path)
        create_summary_pdf(summary_text)
        return "File uploaded successfully"




# List of summarizer servers
summarizer_servers = [
    "http://127.0.0.1:5000",
    "http://127.0.0.1:6000",
    "http://127.0.0.1:7000",
]

def summarize_pdf_on_server(server, text):
    # Send summarization request to server with text as payload
    response = requests.post(server + "/summarize", json={"text": text})
    return response.text
    # response = requests.post(server + "/summarize")
    # return response.text


def summarize_all_pages(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Initialize an empty list to store the summaries
        summaries = []

        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)

        # Extract text from each page and send it to a summarizer server
        for page in pdf_reader.pages:
            text = page.extract_text()

            # Assign page to a summarizer server based on round-robin scheduling
            server = summarizer_servers[len(summaries) % len(summarizer_servers)]

            # Summarize page on the assigned server
            summary = summarize_pdf_on_server(server, text)
            summaries.append(summary)

    return summaries

def create_summary_pdf(summary_text):
    # Create a PDF with the name 'summary.pdf'
    pdf = SimpleDocTemplate("summary.pdf", pagesize=letter)

    # Prepare the styles and add each summary as a separate paragraph
    styles = getSampleStyleSheet()
    flowables = [Paragraph(summary, styles['BodyText']) for summary in summary_text]

    # Build the PDF
    pdf.build(flowables)

server=summarizer_servers[0]
answer="summary.pdf"
#MUTUAL EXCLUSION TO PAGE => When summary generated , that server gets access to the summary.pdf
def request(server_no):
    global token_holder
    if token_holder == -1:  
        token_holder = server_no
        answer[server_no].hastoken = True
        answer[server_no].exec = True
    else:
        answer[server_no].isreq = True
        server.token_q.append(server_no)

def release(server_no):
    global token_holder
    answer[server_no].exec = False

    if server.token_q:  # If there are applicants in the queue
        next_applicant = server.token_q.popleft()
        token_holder = next_applicant
        answer[next_applicant].hastoken = True
        answer[next_applicant].exec = True
    else:
        token_holder = -1  # No one has the token

# # Example usage
# pdf_path = "/Users/shankerltarachandani/Downloads/PlacesInIndia.pdf"
# summary_text = summarize_all_pages(pdf_path)
# create_summary_pdf(summary_text)

if __name__ == "__main__":
    app.run(port=3501)
    print("Server running on port 3501")