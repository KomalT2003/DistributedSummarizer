import os
import Pyro4

@Pyro4.expose
class LeaderServer:
    def __init__(self):
        self.slave_nodes = []
        self.page_texts = []

    def register_slave(self, slave_uri):
        self.slave_nodes.append(slave_uri)
        print(f"Slave node registered: {slave_uri}")

    def add_page_text(self, text):
        self.page_texts.append(text)
        print(f"Page text added. Total: {len(self.page_texts)}")

        # If the number of page texts crosses a threshold, start distributing tasks
        if len(self.page_texts) >= 5:
            print("Triggering task distribution...")
            self.distribute_tasks()
            # Clear the page_texts array for future use
            self.page_texts = []

    def distribute_tasks(self):
        num_files = len(self.page_texts)
        num_slaves = len(self.slave_nodes)
        files_per_slave = num_files // num_slaves
        extra_files = num_files % num_slaves

        start_index = 0
        for slave_uri in self.slave_nodes:
            end_index = start_index + files_per_slave + (1 if extra_files > 0 else 0)
            files_to_process = self.page_texts[start_index:end_index]
            self._send_task_to_slave(slave_uri, files_to_process)
            start_index = end_index
            extra_files -= 1

    def _send_task_to_slave(self, slave_uri, files):
        with Pyro4.Proxy(slave_uri) as slave:
            slave.process_files(files)
            print(f"Sent {len(files)} files to {slave_uri} for processing.")

if __name__ == "__main__":
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(LeaderServer)
    ns.register("leader_server", uri)

    print("Leader Server is ready.")
    daemon.requestLoop()
