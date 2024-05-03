import Pyro4

@Pyro4.expose
class SlaveNode:
    def __init__(self):
        pass

    def process_files(self, files):
        results = []
        for file_name in files:
            # Summarize the text in the file
            summary = self.summarize_text(file_name)
            results.append((file_name, summary))
        return results

    def summarize_text(self, file_name):
        # Your text summarization logic goes here
        # For demonstration purposes, let's just return the file name
        return f"Summary of {file_name}"

if __name__ == "__main__":
    daemon = Pyro4.Daemon()
    ns = Pyro4.locateNS()
    uri = daemon.register(SlaveNode)
    ns.register("slave_node", uri)

    print("Slave Node is ready.")
    daemon.requestLoop()
