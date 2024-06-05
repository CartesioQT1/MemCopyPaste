import win32clipboard
import keyboard
import time


def get_clipboard_text():
    win32clipboard.OpenClipboard()
    clipboard_text = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
    return clipboard_text


def set_clipboard_text(text):
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(text)
    win32clipboard.CloseClipboard()
    

def main():
    keyboard.wait('ctrl+c')
    time.sleep(0.3)
    column_text = get_clipboard_text()
    column_list = column_text.splitlines()
    while column_list:
        item = column_list.pop(0)
        set_clipboard_text(item + "\n")
        print(f"Incollato: {item}")
        keyboard.wait('ctrl+v')
        time.sleep(0.1)


if __name__ == "__main__":
    main()