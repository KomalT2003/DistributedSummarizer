import PyPDF2
import Pyro4

@Pyro4.expose
class TextProcessorServer:
    def __init__(self):
        pass

    def process_text(self, page_num, text):
        # Save text to a file
        file_name = f"page_{page_num}.txt"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(text)
        print(f"Text from page {page_num} saved to {file_name}")

if __name__ == "__main__":
    Pyro4.Daemon.serveSimple(
        {
            TextProcessorServer: "text_processor"
        },
        host="localhost",
        port=9090,
        ns=False
    )