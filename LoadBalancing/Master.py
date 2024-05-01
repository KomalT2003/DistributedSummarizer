

import multiprocessing
import time
from Slave1 import slave_server as slave_server_1
from Slave2 import slave_server as slave_server_2
from Slave3 import slave_server as slave_server_3

# Function to distribute workload to slave servers
def master_server(texts, num_slaves):
    text_queue = multiprocessing.Queue()
    result_queue = multiprocessing.Queue()

    # Start slave processes
    slaves = []
    for i in range(num_slaves):
        if i == 0:
            slave = multiprocessing.Process(target=slave_server_1, args=(text_queue, result_queue, i))
        elif i == 1:
            slave = multiprocessing.Process(target=slave_server_2, args=(text_queue, result_queue, i))
        elif i == 2:
            slave = multiprocessing.Process(target=slave_server_3, args=(text_queue, result_queue, i))
        slave.start()
        slaves.append(slave)

    # Distribute tasks
    for text in texts:
        text_queue.put(text)

    # Stop slave processes
    for _ in range(num_slaves):
        text_queue.put(None)  # Signal to stop

    # Wait for all processes to finish
    for slave in slaves:
        slave.join()

    # Collect results
    summaries = []
    while not result_queue.empty():
        summaries.append(result_queue.get())

    return summaries

# Example usage
if __name__ == "__main__":
    texts = [
        "Page 1: Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
        "Page 2: Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Page 3: Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris.",
        "Page 4: Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Page 5: Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum. "
    ]
    num_slaves = 3

    summaries = master_server(texts, num_slaves)
    for summary, slave_id in summaries:
        print(f"Received from Slave {slave_id + 1}: {summary}")


