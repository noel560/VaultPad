# VaultPad
![Downloads](https://img.shields.io/github/downloads/noel560/VaultPad/total?style=flat-square) ![Stars](https://img.shields.io/github/stars/noel560/VaultPad?style=flat-square) ![Forks](https://img.shields.io/github/forks/noel560/VaultPad?style=flat-square)

VaultPad is a secure text editor designed to allow users to write, edit, and store sensitive information in an encrypted format. This application provides an intuitive interface with the ability to encrypt and decrypt text files using AES encryption, ensuring that your notes and data remain safe from unauthorized access.

## Features
- AES Encryption & Decryption: Protect your sensitive text with AES encryption. Use a password to encrypt and decrypt files.
- Text Editing: Edit your files just like a traditional text editor with basic editing features.
- File Saving & Opening: Easily open and save your encrypted files.
- Help Menu: Get helpful keybindings for common actions such as saving, quitting, encrypting, and decrypting.
- Password Protection: A password is required for encryption and decryption to ensure your files are kept secure.

## How to Use
1. Open File: Open an existing text file that you wish to encrypt or decrypt.
2. Create New File: Start writing a new file, which will be encrypted when saved.
3. Encrypt File: Encrypt your file using AES encryption by providing a password.
4. Decrypt File: Decrypt your file by providing the correct password.
5. Save: Save your file to retain your changes.
6. Exit: Exit the editor, with a prompt warning you if there are unsaved changes.

### Requirements
- python
- pycryptodome
- colorama
- windows-curses

## Installation

1. Install with the Setup file

    ```
    link here
    ```

2. Download manually
    - Clone the repository

        ```
        git clone https://github.com/noel560/VaultPad.git
        cd VaultPad
        ```
    - Install dependencies

        ```
        pip install -r requirements.txt
        ```
    - Run the VaultPad

        ```
        py main.py
        ```