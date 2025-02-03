import yt_dlp
import os
import time
from blessed import Terminal
import sys

term = Terminal()


def cancella_console():
    if os.name == "nt":  # nt indica Windows
        os.system("cls")
    else:  # posix indica macOS o Linux
        os.system("clear")
    
def printl(testo):
    ritardo = 0.01
    for carattere in testo:
        print(carattere, end='', flush=True)
        time.sleep(ritardo)
    print()
    
def printlr(testo):
    ritardo = 0.001
    for carattere in testo:
        print(carattere, end='', flush=True)
        time.sleep(ritardo)
    print()
    
BBLACK = "\033[40m"
BRED = "\033[41m"
BGREEN = "\033[42m"
BYELLOW = "\033[43m"
BBLUE = "\033[44m"
BMAGENTA = "\033[45m"
BACQUA = "\033[46m"
BWHITE = "\033[47m"
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
ACQUA = "\033[36m"
WHITE = "\033[37m"
BT = "\033[0m"

def download_youtube_video(url, output_type='mp4'):
    try:
        printl("Download in corso...")
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        
        download_path = os.path.join(os.getcwd(), 'downloads')
        os.makedirs(download_path, exist_ok=True)

        ydl_opts = {
            'outtmpl': os.path.join(download_path, '%(title)s.%(ext)s'),
            'format': 'bestvideo[vcodec^=avc1][height<=1080]+bestaudio[acodec^=mp4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'quiet': True,  # Riduce al minimo l'output
            'no_warnings': True,  # Nasconde gli avvisi
        }

        if output_type == 'mp3':
            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
                'merge_output_format': 'mp3',
            })
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict.get('title', None)
            sys.stdout = original_stdout
            printl(GREEN + "\nVideo scaricato con successo"+WHITE)
            printl("Cartella: " +YELLOW + str(download_path) + WHITE)
            printl("Titolo: "+RED+ video_title +WHITE + "\n")
            
            modified_title = video_title.replace(" ", "\\ ")
            comando_aprire = "open "  + download_path + "/" + modified_title + "." +  output_type
            os.system(comando_aprire)
    except Exception as e:
        sys.stdout = original_stdout
        printl(f"Errore durante il download: {e}")

def main():
    try:
        cancella_console()
        printlr("")
        printlr(RED + r"__   _______"+WHITE+r" ____                      _                 _           ")
        printlr(RED + r"\ \ / /_   _"+WHITE+r"|  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ ")
        printlr(RED + r" \ V /  | | "+WHITE+r"| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|")
        printlr(RED + r"  | |   | | "+WHITE+r"| |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   ")
        printlr(RED + r"  |_|   |_| "+WHITE+r"|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   ")                                                              
        printlr("")

        url_video = input("Incolla l'url: "+RED)
        
        if url_video == "":
            main()
        elif url_video == "q" or url_video == "e" or url_video == "quit" or url_video == "exit":
            cancella_console()
            quit()
        elif "https://www.youtube.com/watch?" not in url_video:
            print("\n+---------------------------------+\n| ERRORE: Inserisci un url valido |\n+---------------------------------+" + WHITE)
            time.sleep(2.5)
            main()

    except KeyboardInterrupt:
        cancella_console()
        quit()
        
    def scelta_modalità():
        cancella_console()
        print("")
        print(RED + r"__   _______"+WHITE+r" ____                      _                 _           ")
        print(RED + r"\ \ / /_   _"+WHITE+r"|  _ \  _____      ___ __ | | ___   __ _  __| | ___ _ __ ")
        print(RED + r" \ V /  | | "+WHITE+r"| | | |/ _ \ \ /\ / / '_ \| |/ _ \ / _` |/ _` |/ _ \ '__|")
        print(RED + r"  | |   | | "+WHITE+r"| |_| | (_) \ V  V /| | | | | (_) | (_| | (_| |  __/ |   ")
        print(RED + r"  |_|   |_| "+WHITE+r"|____/ \___/ \_/\_/ |_| |_|_|\___/ \__,_|\__,_|\___|_|   ")                                                              
        print("")
        print("Incolla l'url: "+RED+url_video+WHITE)
        
        
    opzioni = ["Audio e Video", "Solo Audio"]
    index = 0 
    
    with term.cbreak(), term.hidden_cursor():
        while True:
            try:
                print(term.clear)
                scelta_modalità()
                print("")
                print("Seleziona la modalità:\n(Usa "+RED+"←"+" "+"→"+WHITE+" per muoverti e "+RED+"↵"+WHITE+" per confermare)")

                # Calcola la lunghezza totale del contenuto con i trattini
                contenuto = " - ".join(opzioni)
                larghezza = len(contenuto) + 2  # Spazi aggiuntivi per il bordo

                # Stampa il riquadro superiore
                print("┌" + "─" * larghezza + "┐")

                # Stampa le opzioni con i trattini
                print("│ ", end="")
                for i, opzione in enumerate(opzioni):
                    if i == index:
                        print(BRED + opzione + BT, end="")
                    else:
                        print(opzione, end="")
                    if i < len(opzioni) - 1:  # Aggiunge un trattino tra le opzioni
                        print(" ~ ", end="")
                print(" │")  # Chiude la riga

                # Stampa il riquadro inferiore
                print("└" + "─" * larghezza + "┘")
                print("\n")  # Spaziatura

                # Legge l'input dell'utente
                key = term.inkey()

                if key.name == "KEY_LEFT" or key.name == "KEY_DOWN":
                    index = (index - 1) % len(opzioni)
                elif key.name == "KEY_RIGHT" or key.name == "KEY_UP":
                    index = (index + 1) % len(opzioni)
                elif key.name == "KEY_ENTER" or key.name == "SPACE":
                    if index == 0:
                        #video e audio
                        tipo_video = "mp4"
                    elif index == 1:
                        #solo audio
                        tipo_video = "mp3"
                    break
                elif key == "q":
                    break
            except KeyboardInterrupt:
                cancella_console()
                quit()
    
    download_youtube_video(url_video, tipo_video)
        

if __name__ == '__main__':
    main()