import os
import sys
import time
import shutil
import mimetypes
import subprocess
import platform
from pathlib import Path


class Colors:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[91m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"

    @classmethod
    def color(cls, text, value):
        if sys.stdout.isatty():
            return f"{value}{text}{cls.RESET}"
        return text


class FileExplorer:
    VERSION = "0.0.2"
    AUTHOR = "N9uf_S"

    def __init__(self):
        self.system_name = self.detect_system()
        self.current_dir = self.default_start_dir()
        self.history = []
        self.active_filter = None

    def detect_system(self):
        if Path("/data/data/com.termux/files/home").exists() or Path("/storage/emulated/0").exists():
            return "Android"

        system = platform.system().lower()

        if "windows" in system:
            return "Windows"
        if "linux" in system:
            return "Linux"
        if "darwin" in system or "mac" in system:
            return "macOS"

        return platform.system()

    def default_start_dir(self):
        android_storage = Path("/storage/emulated/0")
        if android_storage.exists():
            return android_storage.resolve()
        return Path.home().resolve()

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def line(self, char="═", length=78):
        return char * length

    def pause(self, message=None):
        if message is None:
            message = Colors.color("\n[ Entrée ] Continuer...", Colors.YELLOW)
        input(message)

    def human_size(self, size):
        units = ["o", "Ko", "Mo", "Go", "To"]
        size = float(size)
        index = 0

        while size >= 1024 and index < len(units) - 1:
            size /= 1024
            index += 1

        return f"{size:.2f} {units[index]}"

    def file_type(self, path):
        mime, _ = mimetypes.guess_type(str(path))

        if mime:
            if mime.startswith("image"):
                return "image"
            if mime.startswith("video"):
                return "vidéo"
            if mime.startswith("audio"):
                return "audio"
            if mime.startswith("text"):
                return "texte"
            if mime == "application/pdf":
                return "pdf"

        ext = path.suffix.lower()

        image_exts = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp"}
        video_exts = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".3gp"}
        audio_exts = {".mp3", ".wav", ".ogg", ".aac", ".flac", ".m4a"}
        text_exts = {".txt", ".py", ".json", ".html", ".css", ".js", ".md", ".csv", ".log"}
        pdf_exts = {".pdf"}

        if ext in image_exts:
            return "image"
        if ext in video_exts:
            return "vidéo"
        if ext in audio_exts:
            return "audio"
        if ext in text_exts:
            return "texte"
        if ext in pdf_exts:
            return "pdf"

        return "fichier"

    def boot_screen(self):
        self.clear()

        banner = f"""
{Colors.color("███╗   ██╗  █████╗  ██╗   ██╗ ███████╗", Colors.GREEN)}
{Colors.color("████╗  ██║ ██╔══██╗ ██║   ██║ ██╔════╝", Colors.GREEN)}
{Colors.color("██╔██╗ ██║ ╚██████║ ██║   ██║ █████╗  ", Colors.GREEN)}
{Colors.color("██║╚██╗██║  ╚═══██║ ██║   ██║ ██╔══╝  ", Colors.GREEN)}
{Colors.color("██║ ╚████║  █████╔╝ ╚██████╔╝ ██║     ", Colors.GREEN)}
{Colors.color("╚═╝  ╚═══╝  ╚════╝   ╚═════╝  ╚═╝     ", Colors.GREEN)}

{Colors.color("EXPLORATEUR DE FICHIERS PYTHON", Colors.CYAN)}
{Colors.color("Version 0.0.2", Colors.YELLOW)}
{Colors.color("Signature : N9uf_S", Colors.MAGENTA)}
"""
        print(banner)

        steps = [
            "Analyse du système",
            "Chargement des modules",
            "Préparation de l'explorateur",
            "Détection de la plateforme",
            "Initialisation de l'interface"
        ]

        total = 28
        progress = 0

        for i, step in enumerate(steps, start=1):
            target = int((i / len(steps)) * total)

            while progress < target:
                progress += 1
                bar = "█" * progress + "░" * (total - progress)
                pct = int(progress / total * 100)
                print(
                    "\r"
                    + Colors.color("[BOOT] ", Colors.YELLOW)
                    + Colors.color(bar, Colors.GREEN)
                    + " "
                    + Colors.color(f"{pct:>3}%", Colors.CYAN),
                    end="",
                    flush=True,
                )
                time.sleep(0.03)

            print()
            print(Colors.color(f"  -> {step}", Colors.WHITE))
            time.sleep(0.12)

        print(Colors.color(f"\n[SYSTÈME] {self.system_name}", Colors.MAGENTA))
        print(Colors.color(self.line(), Colors.CYAN))

    def header(self):
        banner = f"""
{Colors.color("███╗   ██╗  █████╗  ███████╗", Colors.GREEN)}
{Colors.color("████╗  ██║ ██╔══██╗ ██╔════╝", Colors.GREEN)}
{Colors.color("██╔██╗ ██║ ╚██████║ ███████╗", Colors.GREEN)}
{Colors.color("██║╚██╗██║  ╚═══██║ ╚════██║", Colors.GREEN)}
{Colors.color("██║ ╚████║  █████╔╝ ███████║", Colors.GREEN)}
{Colors.color("╚═╝  ╚═══╝  ╚════╝  ╚══════╝", Colors.GREEN)}
"""
        print(banner)
        print(Colors.color("EXPLORATEUR DE FICHIERS PYTHON", Colors.CYAN))
        print(Colors.color("Version 0.0.2", Colors.YELLOW))
        print(Colors.color("Signature : N9uf_S", Colors.MAGENTA))
        print(Colors.color(self.line(), Colors.CYAN))
        print(
            f"{Colors.color('[Plateforme]', Colors.YELLOW)} {self.system_name}   "
            f"{Colors.color('[Auteur]', Colors.YELLOW)} {self.AUTHOR}   "
            f"{Colors.color('[Filtre]', Colors.YELLOW)} {self.active_filter if self.active_filter else 'aucun'}"
        )
        print(Colors.color(self.line(), Colors.CYAN))

    def list_items(self):
        try:
            items = list(self.current_dir.iterdir())
        except PermissionError:
            print(Colors.color("\n[!] Permission refusée pour ce dossier.", Colors.RED))
            self.pause()
            return []

        dirs = sorted([item for item in items if item.is_dir()], key=lambda p: p.name.lower())
        files = sorted([item for item in items if item.is_file()], key=lambda p: p.name.lower())

        if self.active_filter:
            files = [f for f in files if self.file_type(f) == self.active_filter]

        return dirs + files

    def print_menu(self, items):
        self.clear()
        self.header()
        print(f"{Colors.color('[Dossier courant]', Colors.YELLOW)} {self.current_dir}")
        print(Colors.color(self.line("─"), Colors.CYAN))

        if self.current_dir.parent != self.current_dir:
            print(" 0. [..] Revenir au dossier parent")

        if not items:
            print(" -- Aucun élément trouvé dans ce dossier --")
        else:
            for index, item in enumerate(items, start=1):
                if item.is_dir():
                    print(f" {index:>2}. {Colors.color('[DIR ]', Colors.BLUE)} {item.name}")
                else:
                    print(
                        f" {index:>2}. {Colors.color('[FILE]', Colors.GREEN)} "
                        f"{item.name} {Colors.color('(' + self.file_type(item) + ')', Colors.MAGENTA)}"
                    )

        print(Colors.color(self.line("─"), Colors.CYAN))
        print(Colors.color("COMMANDES DISPONIBLES", Colors.WHITE))
        print(Colors.color(self.line("─"), Colors.CYAN))
        print(" i<num>  : afficher les infos d'un élément")
        print(" f       : appliquer un filtre")
        print(" r       : retirer le filtre")
        print(" h       : afficher l'historique")
        print(" q       : quitter")
        print(Colors.color(self.line(), Colors.CYAN))

    def show_info(self, path):
        path = Path(path)

        if not path.exists():
            print(Colors.color("\n[!] Élément introuvable.", Colors.RED))
            self.pause()
            return

        print()
        print(Colors.color(self.line("─"), Colors.CYAN))
        print(Colors.color("INFORMATIONS", Colors.WHITE))
        print(Colors.color(self.line("─"), Colors.CYAN))
        print(f" Nom       : {path.name}")
        print(f" Chemin    : {path.resolve()}")
        print(f" Type      : {'dossier' if path.is_dir() else self.file_type(path)}")

        if path.is_file():
            print(f" Taille    : {self.human_size(path.stat().st_size)}")

        print(Colors.color(self.line("─"), Colors.CYAN))
        self.pause()

    def show_history(self):
        self.clear()
        self.header()
        print(Colors.color("HISTORIQUE", Colors.WHITE))
        print(Colors.color(self.line("─"), Colors.CYAN))

        if not self.history:
            print(" Aucun fichier ouvert pour le moment.")
        else:
            for index, entry in enumerate(self.history, start=1):
                print(f" {index:>2}. {entry}")

        print(Colors.color(self.line("─"), Colors.CYAN))
        self.pause()

    def choose_filter(self):
        self.clear()
        self.header()
        print(Colors.color("CHOIX DU FILTRE", Colors.WHITE))
        print(Colors.color(self.line("─"), Colors.CYAN))
        print(" 1. image")
        print(" 2. vidéo")
        print(" 3. audio")
        print(" 4. pdf")
        print(" 5. texte")
        print(" 0. annuler")
        print(Colors.color(self.line("─"), Colors.CYAN))

        choice = input(Colors.color(">>> Ton choix : ", Colors.YELLOW)).strip()

        filters = {
            "1": "image",
            "2": "vidéo",
            "3": "audio",
            "4": "pdf",
            "5": "texte",
        }

        return filters.get(choice)

    def command_exists(self, cmd):
        return shutil.which(cmd) is not None

    def open_file(self, path):
        path = Path(path)

        if not path.exists():
            print(Colors.color("\n[!] Fichier introuvable.", Colors.RED))
            self.pause()
            return

        try:
            if self.system_name == "Android":
                if self.command_exists("termux-open"):
                    subprocess.run(["termux-open", str(path)], check=False)
                elif self.command_exists("xdg-open"):
                    subprocess.run(["xdg-open", str(path)], check=False)
                else:
                    print(Colors.color("\n[!] Impossible d'ouvrir le fichier sur Android.", Colors.RED))
                    print(" Installe termux-api puis exécute : termux-setup-storage")
                    self.pause()
                    return

            elif self.system_name == "Windows":
                os.startfile(str(path))  # type: ignore[attr-defined]

            elif self.system_name == "Linux":
                if self.command_exists("xdg-open"):
                    subprocess.run(["xdg-open", str(path)], check=False)
                else:
                    print(Colors.color("\n[!] xdg-open est introuvable sur ce système.", Colors.RED))
                    self.pause()
                    return

            elif self.system_name == "macOS":
                subprocess.run(["open", str(path)], check=False)

            else:
                print(Colors.color("\n[!] Système non supporté.", Colors.RED))
                self.pause()
                return

            self.history.append(str(path.resolve()))
            print(Colors.color(f"\n[OK] Ouverture : {path.name}", Colors.GREEN))
            print(Colors.color(f"[TYPE] {self.file_type(path)}", Colors.CYAN))

        except Exception as exc:
            print(Colors.color(f"\n[ERREUR] {exc}", Colors.RED))

        self.pause()

    def run(self):
        while True:
            items = self.list_items()
            self.print_menu(items)
            choice = input(Colors.color(">>> Choix : ", Colors.YELLOW)).strip().lower()

            if choice == "q":
                self.clear()
                self.header()
                print(Colors.color("Fermeture du module Explorateur...", Colors.RED))
                print(Colors.color(self.line(), Colors.CYAN))
                break

            if choice == "f":
                new_filter = self.choose_filter()
                if new_filter:
                    self.active_filter = new_filter
                continue

            if choice == "r":
                self.active_filter = None
                continue

            if choice == "h":
                self.show_history()
                continue

            if choice == "0":
                if self.current_dir.parent != self.current_dir:
                    self.current_dir = self.current_dir.parent
                continue

            if choice.startswith("i"):
                number_text = choice[1:].strip()

                if number_text.isdigit():
                    number = int(number_text)
                    if 1 <= number <= len(items):
                        self.show_info(items[number - 1])
                    else:
                        print(Colors.color("\n[!] Numéro invalide.", Colors.RED))
                        self.pause()
                else:
                    print(Colors.color("\n[!] Commande invalide.", Colors.RED))
                    self.pause()
                continue

            if choice.isdigit():
                number = int(choice)

                if 1 <= number <= len(items):
                    selected = items[number - 1]
                    if selected.is_dir():
                        self.current_dir = selected.resolve()
                    else:
                        self.open_file(selected)
                else:
                    print(Colors.color("\n[!] Numéro invalide.", Colors.RED))
                    self.pause()
                continue

            print(Colors.color("\n[!] Choix invalide.", Colors.RED))
            self.pause()


if __name__ == "__main__":
    app = FileExplorer()
    app.boot_screen()
    app.pause(Colors.color("\n[ Entrée ] Lancer l'explorateur...", Colors.YELLOW))
    app.run()
