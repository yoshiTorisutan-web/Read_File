import sys
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import openai

class Watcher:
    DIRECTORY_TO_WATCH = "/chemin/vers/le/dossier"

    def __init__(self):
        self.observer = Observer()

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.DIRECTORY_TO_WATCH, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(5)
        except:
            self.observer.stop()
            print("Observer Stopped")

        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if event.is_directory:
            return None
        elif event.src_path.endswith('.txt'):
            try:
                with open(event.src_path, 'r') as f:
                    content = f.read()

                # Génération du résumé avec GPT-3 (par exemple)
                # Vous devez d'abord configurer votre clé API pour cela
                openai.api_key = 'VOTRE_CLE_API'
                response = openai.Completion.create(engine="davinci", prompt=f"Résumez ce texte:\n{content}", max_tokens=150)
                summary = response.choices[0].text.strip()

                with open(event.src_path.replace('.txt', '_resume.txt'), 'w') as f:
                    f.write(summary)

            except Exception as e:
                print(f"Error: {e}")

if __name__ == '__main__':
    w = Watcher()
    w.run()
