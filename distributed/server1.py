from flask import Flask, request, jsonify
from transformers import BartForConditionalGeneration, BartTokenizer
from transformers import pipeline
import torch
import os
import PyPDF2
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
import requests

app = Flask(__name__)

@app.route("/",methods=["GET"])
def home():
    return "Hello, World!"

@app.route("/summarize", methods=["POST"])
def summarize_pdf():
        text=request.json["text"]
        # Initialize the BART model and tokenizer
        model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
        tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
        
        # Tokenize the text
        inputs = tokenizer.encode("summarize: " + text, return_tensors="pt", max_length=1024, truncation=True)
        
        # Generate summary using the model
        summary_ids = model.generate(inputs, max_length=150, min_length=50, length_penalty=2.0, num_beams=4, early_stopping=True)
        summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
        print("Access of page granted to server 1 , cannot be accessed by other servers")
        return summary
import threading

def count_the_occurrences(chunk, chunk_number):
    
    chunk_text = "\n".join(chunk)
    count = chunk_text.lower().split().count('the')
    return count

def process_text_in_chunks(text, chunk_size):
    lines = text.split('\n')
    total_lines = len(lines)
    chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]

    threads = []

    for i, chunk in enumerate(chunks):
        thread = threading.Thread(target=count_the_occurrences, args=(chunk, i + 1))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

if __name__ == "__main__":
    app.run(port=5000)
