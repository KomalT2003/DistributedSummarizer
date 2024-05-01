


import multiprocessing
import random
import time

# Function to simulate text summarization
def summarize_text(text):
    # Simulate summarization process
    time.sleep(random.uniform(1, 3))
    return f"Summary of '{text[:20]}...'"

# Function to be executed by the second slave server
def slave_server(text_queue, result_queue, slave_id):
    while True:
        text = text_queue.get()
        if text is None:
            break
        summary = summarize_text(text)
        result_queue.put((summary, slave_id))

# Example usage
if __name__ == "__main__":
    text_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()
    slave_id = 1

    while True:
        text = text_queue.get()
        if text is None:
            break
        summary = summarize_text(text)
        result_queue.put((summary, slave_id))

