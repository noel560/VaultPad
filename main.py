import os
from colorama import Fore, Style, init
import sys
import time
from tkinter import filedialog, messagebox
import editor

init(autoreset=True)

def display():
    print(Fore.LIGHTYELLOW_EX + "Welcome to VaultPad!")
    print(Fore.LIGHTYELLOW_EX + "Your secure note-taking application.")
    print("")
    print(Fore.GREEN + "Please select an option:")
    print(Fore.LIGHTBLACK_EX + "--------------------")
    print(
        Fore.LIGHTWHITE_EX + "[" + Fore.LIGHTGREEN_EX + "1" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Open File" +
        "\n" +
        Fore.LIGHTWHITE_EX + "[" + Fore.LIGHTGREEN_EX + "2" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Create New File" +
        "\n" +
        Fore.LIGHTWHITE_EX + "[" + Fore.LIGHTGREEN_EX + "3" + Fore.LIGHTWHITE_EX + "]" + Fore.LIGHTGREEN_EX + " Exit")
    print(Fore.LIGHTBLACK_EX + "--------------------")

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
        editor.curses_editor(file_path, content)

def create_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        editor.curses_editor(file_path)

def main():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        display()
        choice = input(Fore.LIGHTCYAN_EX + "> " + Style.RESET_ALL)
        if choice == '1':
            open_file()
        elif choice == '2':
            create_file()
        elif choice == '3':
            break
        else:
            print(Fore.RED + "Invalid option. Please try again.")
            time.sleep(1)


if __name__ == "__main__":
    main()