import threading

def count_the_occurrences(chunk, chunk_number):
    
    chunk_text = "\n".join(chunk)
    count = chunk_text.lower().split().count('the')
    print(f"Chunk {chunk_number}: Number of 'the' occurrences = {count}")
    return count

def process_text_in_chunks(text, chunk_size):
    lines = text.split('\n')
    total_lines = len(lines)
    chunks = [lines[i:i + chunk_size] for i in range(0, total_lines, chunk_size)]
    print("No of chunks extracted and no.of threads to be formed: ", len(chunks))

    threads = []

    for i, chunk in enumerate(chunks):
        thread = threading.Thread(target=count_the_occurrences, args=(chunk, i + 1))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()