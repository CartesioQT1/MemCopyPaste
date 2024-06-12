import win32clipboard
import PySimpleGUI as sg
import threading
import keyboard
import time


def check_clip():
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.CloseClipboard()
        return True
    except Exception as e:
        print(f"Errore nell'accesso alla clipboard: {e}")
        return False

def run_safe(func):
    if check_clip():
        return func()
    else:
        #time.sleep(0.3)
        return run_safe(func)

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
        

def flush_clipboard():
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.CloseClipboard()


def get_next(column_list):
    run_safe(lambda: set_clipboard_text(column_list[0]))
    keyboard.wait('ctrl+v')
    while column_list:
        item = column_list.pop(0)
        run_safe(lambda: set_clipboard_text(item + "\n"))
        keyboard.wait('ctrl+v')
        run_safe(flush_clipboard)
    return True

def script():
    just_flushed = True
    while True:
        if program_running:    
            keyboard.wait('ctrl+c')
            time.sleep(0.3)
            column_text = run_safe(get_clipboard_text)
            column_list = column_text.splitlines()
            get_next(column_list)
            just_flushed = False
        else:
            if not just_flushed:
                run_safe(flush_clipboard)
                just_flushed = True


def main():
    layout = [
        [sg.Text('Controllo del Programma')],
        [sg.Button('Run/Stop', key='-STARTPAUSE-', button_color=('white','red'))],
    ]

    window = sg.Window('MemCP', layout)

    global program_running
    program_running = False
    program_thread = threading.Thread(target=script, daemon=True)
    program_thread.start()
    
    while True:
        event, values = window.read(timeout=100)

        if event == sg.WIN_CLOSED:
            break

        if event == '-STARTPAUSE-':
            program_running = not program_running
            window['-STARTPAUSE-'].update(button_color=('white', 'green' if program_running else 'red'))        

    window.close()


if __name__ == "__main__":
    main()
