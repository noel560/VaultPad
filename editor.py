import curses
import os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import hashlib

SAVE_KEY = 19  # Ctrl+S
EXIT_KEY = 17  # Ctrl+Q
ENCRYPT_KEY = 5  # Ctrl+E
DECRYPT_KEY = 4  # Ctrl+D


def derive_key(password):
    return hashlib.sha256(password.encode()).digest()


def encrypt_text(text, password):
    key = derive_key(password)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(text.encode('utf-8'), AES.block_size))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ":" + ct


def decrypt_text(enc_text, password):
    try:
        key = derive_key(password)
        iv, ct = enc_text.split(":")
        iv = base64.b64decode(iv)
        ct = base64.b64decode(ct)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8'), None
    except Exception as e:
        return "", "Decryption failed. Incorrect password or corrupted data."


def curses_editor(file_path=None, initial_text=""):
    lines = initial_text.splitlines() if initial_text else [""]
    saved_lines = list(lines)  # for checking unsaved changes

    def main(stdscr):
        nonlocal lines, saved_lines
        curses.curs_set(1)
        stdscr.keypad(True)
        max_y, max_x = stdscr.getmaxyx()

        cursor_x = 0
        cursor_y = 0

        def prompt_password(prompt):
            curses.echo(False)
            win = curses.newwin(3, max_x - 4, max_y // 2 - 1, 2)
            win.box()
            win.addstr(1, 2, prompt)
            win.refresh()
            pw = ""
            while True:
                ch = stdscr.get_wch()
                if isinstance(ch, str) and ch == '\n':
                    break
                elif isinstance(ch, str) and ch in ('\x08', '\x7f'):
                    pw = pw[:-1]
                elif isinstance(ch, str) and ch.isprintable():
                    pw += ch
                win.addstr(1, len(prompt) + 2, '*' * len(pw) + ' ')
                win.refresh()
            return pw

        def has_unsaved_changes():
            return lines != saved_lines

        while True:
            stdscr.clear()

            # Draw text content
            for i, line in enumerate(lines):
                if i < max_y - 2:
                    stdscr.addstr(i, 0, line[:max_x-1])

            # Draw status/help bar
            status = "Ctrl+S: Save  Ctrl+Q: Quit  Ctrl+E: Encrypt  Ctrl+D: Decrypt"
            if has_unsaved_changes():
                status = "[UNSAVED] " + status
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(max_y - 1, 0, status[:max_x - 1] + " " * (max_x - len(status) - 1))
            stdscr.attroff(curses.color_pair(1))

            stdscr.move(cursor_y, cursor_x)
            stdscr.refresh()

            key = stdscr.get_wch()  # Unicode character input

            if isinstance(key, str):
                if key == '\x13':  # Ctrl+S
                    if file_path:
                        with open(file_path, "w", encoding="utf-8") as f:
                            f.write("\n".join(lines))
                            saved_lines = list(lines)
                elif key == '\x11':  # Ctrl+Q
                    if has_unsaved_changes():
                        stdscr.addstr(max_y - 3, 0, "You have unsaved changes. Press Ctrl+Q again to quit without saving.")
                        stdscr.refresh()
                        confirm_key = stdscr.get_wch()
                        if confirm_key == '\x11':
                            break
                    else:
                        break
                elif key == '\x05':  # Ctrl+E - Encrypt
                    password = prompt_password("Enter password to encrypt: ")
                    encrypted = encrypt_text("\n".join(lines), password)
                    lines = encrypted.splitlines()
                elif key == '\x04':  # Ctrl+D - Decrypt
                    password = prompt_password("Enter password to decrypt: ")
                    decrypted, error = decrypt_text("\n".join(lines), password)
                    if error:
                        stdscr.addstr(max_y - 3, 0, error[:max_x - 1])
                        stdscr.refresh()
                        stdscr.getch()
                    else:
                        lines = decrypted.splitlines()
                elif key == '\n':  # Enter
                    current = lines[cursor_y]
                    new_line = current[cursor_x:]
                    lines[cursor_y] = current[:cursor_x]
                    lines.insert(cursor_y + 1, new_line)
                    cursor_y += 1
                    cursor_x = 0
                elif key in ('\x08', '\x7f'):  # Backspace
                    if cursor_x > 0:
                        line = lines[cursor_y]
                        lines[cursor_y] = line[:cursor_x - 1] + line[cursor_x:]
                        cursor_x -= 1
                    elif cursor_y > 0:
                        prev_len = len(lines[cursor_y - 1])
                        lines[cursor_y - 1] += lines[cursor_y]
                        lines.pop(cursor_y)
                        cursor_y -= 1
                        cursor_x = prev_len
                elif key.isprintable():
                    line = lines[cursor_y]
                    lines[cursor_y] = line[:cursor_x] + key + line[cursor_x:]
                    cursor_x += len(key)
            elif isinstance(key, int):
                if key == curses.KEY_LEFT:
                    if cursor_x > 0:
                        cursor_x -= 1
                    elif cursor_y > 0:
                        cursor_y -= 1
                        cursor_x = len(lines[cursor_y])
                elif key == curses.KEY_RIGHT:
                    if cursor_x < len(lines[cursor_y]):
                        cursor_x += 1
                    elif cursor_y + 1 < len(lines):
                        cursor_y += 1
                        cursor_x = 0
                elif key == curses.KEY_UP:
                    if cursor_y > 0:
                        cursor_y -= 1
                        cursor_x = min(cursor_x, len(lines[cursor_y]))
                elif key == curses.KEY_DOWN:
                    if cursor_y + 1 < len(lines):
                        cursor_y += 1
                        cursor_x = min(cursor_x, len(lines[cursor_y]))

    curses.wrapper(init_colors_and_run(main))


def init_colors_and_run(func):
    def wrapper(stdscr):
        curses.start_color()
        curses.use_default_colors()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        func(stdscr)
    return wrapper
