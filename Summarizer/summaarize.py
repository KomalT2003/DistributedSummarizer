import PyPDF2
from transformers import BartForConditionalGeneration, BartTokenizer
from io import BytesIO
from summarizer import Summarizer

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet


def summarize_pdf(text):
        # Initialize the BART model and tokenizer
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        
        # Tokenize the text
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        
        # Generate summary using the model
        summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        
        return summary


def summarize_all_pages(pdf_path):
    # Open the PDF file
    with open(pdf_path, 'rb') as file:
        # Create a PDF reader object
        pdf_reader = PyPDF2.PdfReader(file)
        
        # Initialize an empty list to store the summaries
        summaries = []
        
        # Extract text from each page and generate summary
        for page in pdf_reader.pages:
            text = page.extract_text()
            summary = summarize_pdf(text)
            summaries.append(summary)
        
        return summaries

def clean_text(text):
    # Remove extra spaces and newlines
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

def create_summary_pdf(summary_text):
    # Create a PDF with the name 'summary.pdf'
    pdf = SimpleDocTemplate("summary.pdf", pagesize=letter)

    # Prepare the styles and add each summary as a separate paragraph
    styles = getSampleStyleSheet()
    flowables = [Paragraph(summary, styles['BodyText']) for summary in summary_text]

    # Build the PDF
    pdf.build(flowables)



# Example usage
pdf_path = "/Users/shankerltarachandani/Downloads/PlacesInIndia.pdf"  # Replace with the path to your PDF file
summary_text = summarize_all_pages(pdf_path)
print(summary_text)
# final_summary = ""
# for summary in summary_text:
#     final_summary += "<p>" + summary + "</p>"
create_summary_pdf(summary_text)