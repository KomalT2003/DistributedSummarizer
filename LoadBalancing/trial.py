import threading
import queue

class Master:
    def __init__(self, pages):
        self.pages = pages
        self.page_queue = queue.Queue()
        self.slave_threads = []

    def start(self):
        # Fill the page queue with pages
        for page in self.pages:
            self.page_queue.put(page)

        # Create and start slave threads
        for i in range(3):  # Change the number of slaves as per your requirement
            slave_thread = threading.Thread(target=self.slave_worker)
            slave_thread.start()
            self.slave_threads.append(slave_thread)

        # Wait for all pages to be processed
        self.page_queue.join()

        # Stop slave threads
        for slave_thread in self.slave_threads:
            self.page_queue.put(None)  # Signal to stop the slave thread
            slave_thread.join()

    def slave_worker(self):
        while True:
            page = self.page_queue.get()
            if page is None:
                break  # Stop the slave thread

            # Process the page (summarization logic)
            print(f"Processing page: {page}")

            self.page_queue.task_done()

# Usage example
pages = [1, 2, 3, 4, 5]  # Replace with your actual pages
master = Master(pages)
master.start()