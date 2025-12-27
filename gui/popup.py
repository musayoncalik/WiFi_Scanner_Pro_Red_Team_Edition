import tkinter as tk
from tkinter import messagebox
import threading
import logging

log = logging.getLogger(__name__)

def notify_async(title, message, msg_type='info'):
    def _show():
        try:
            root = tk.Tk()
            root.withdraw()
            root.attributes('-topmost', True)
            
            if msg_type == 'info':
                messagebox.showinfo(title, message, parent=root)
            elif msg_type == 'warning':
                messagebox.showwarning(title, message, parent=root)
            elif msg_type == 'error':
                messagebox.showerror(title, message, parent=root)
            elif msg_type == 'question':
                return messagebox.askyesno(title, message, parent=root)
            else:
                messagebox.showinfo(title, message, parent=root)
            
            root.destroy()
        except Exception as e:
            log.exception("Popup gösterim hatası: %s", e)
    
    t = threading.Thread(target=_show, daemon=True)
    t.start()

def show_error(title, message):
    notify_async(title, message, 'error')

def show_warning(title, message):
    notify_async(title, message, 'warning')

def show_info(title, message):
    notify_async(title, message, 'info')
