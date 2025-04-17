import sys
import tkinter
from tkinter import *
from tkinter import filedialog
import datetime
import time
from tkinter import messagebox
import subprocess
import threading
import tkinter.ttk
import os
import ctypes
from subprocess import Popen, STDOUT


def destroy_self():
    if sys.platform.startswith('win'):
        script_path = os.path.abspath(__file__)
        deletion_script = f"""@echo off
timeout /t 1 /nobreak > nul
del "{script_path}"
del "%~f0"
"""
        batch_file_path = os.path.join(os.path.dirname(script_path), "delete_self.bat")
        with open(batch_file_path, "w") as f:
            f.write(deletion_script)
        subprocess.Popen([batch_file_path], creationflags=subprocess.CREATE_NO_WINDOW)
    else:
        messagebox.showerror("Unsupported OS", "Self-deletion on closing is only supported on Windows.")

def is_admin():
    try:
        return ctypes.windll.shell.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    messagebox.showinfo("Administrator Rights Recommended", "This program works best while run as admin. Some files may not be copied otherwise. Click OK to continue.")

w = tkinter.Tk()
w.geometry("400x250")
w.title("Copy Assistant")
w.resizable(False, False)

w.configure(bg="#f0f0f0")

source_value = tkinter.StringVar()
destination_value = tkinter.StringVar()
output_file = "history.txt"

def submit():
    xflags = "/h/e/r/k/y/j"
    rflags = "/E /XC /XN /XO"

    header_x = "xcopy"
    header_r = "robocopy"
    source = source_value.get()
    destination = destination_value.get()
    clicked_value = clicked.get()

    if not (":" in source and ":" in destination):
        messagebox.showerror("Error", "Source and Destination paths must include a drive letter (e.g., C:\\).")
        return

    if source == destination:
        messagebox.showerror("Error", "Source and Destination paths must be different.")
        return

    popup = Toplevel(w)
    popup.title("Copying...")
    popup.geometry("300x120")
    Label(popup, text="Copying files...").pack(pady=5)
    progress_bar = tkinter.ttk.Progressbar(popup, mode='indeterminate')
    progress_bar.pack(pady=5)
    progress_bar.start()
    time_label = Label(popup, text="Estimated time remaining: Calculating...", bg=popup.cget('bg'))
    time_label.pack(pady=5)

    start_time = time.time()

    def copy_thread():
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        if not os.path.exists(output_file):
            create_file = messagebox.askyesno("Create File?", f"{output_file} does not exist. Would you like to create it?")
            if create_file:
                open(output_file, 'a').close()
            else:
                popup.destroy()
                return

        with open(output_file, "a") as f:
            f.write(f"Copy started at: {current_time}\n")
            original_stdout = sys.stdout
            sys.stdout = f

            if clicked_value.lower() == "local":
                print("local")
                print(source)
                print(destination)
                quoted_source = f'"{source}"'
                quoted_destination = f'"{destination}"'
                command = str(header_x + " " + quoted_source + " " + quoted_destination + " " + xflags)
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result.stdout)
                    print(result.stderr)
                except Exception as e:
                    print(f"Error executing command: {e}")
            elif clicked_value.lower() == "network":
                print("Network")
                print(source)
                print(destination)
                command = str(header_r + " " + source + " " + destination + " " + rflags)
                try:
                    result = subprocess.run(command, shell=True, capture_output=True, text=True)
                    print(result.stdout)
                    print(result.stderr)
                except Exception as e:
                    print(f"Error executing command: {e}")
            else:
                print("Invalid selection.")

            sys.stdout = original_stdout
        popup.destroy()

        end_time = time.time()
        elapsed_time = end_time - start_time
        messagebox.showinfo("Copy Complete", f"Copy completed in {elapsed_time:.2f} seconds.")

    threading.Thread(target=copy_thread).start()

clicked = StringVar()
clicked.set("Local")
drop = OptionMenu(w, clicked, "Local", "Network")
drop.config(bg="#e0e0e0", highlightthickness=0)

source_label = tkinter.Label(w, text='Source:', bg="#f0f0f0", font=('Arial', 10))
source_entry = tkinter.Entry(w, textvariable=source_value, font=('Arial', 10), bg="white")
destination_label = tkinter.Label(w, text='Destination:', bg="#f0f0f0", font=('Arial', 10))
destination_entry = tkinter.Entry(w, textvariable=destination_value, font=('Arial', 10), bg="white")

sub_btn = tkinter.Button(w, text='Submit', command=submit, bg="#4CAF50", fg="white", font=('Arial', 10, 'bold'))

source_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
source_entry.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
destination_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
destination_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
drop.grid(row=2, column=1, padx=10, pady=5, sticky="ew")
sub_btn.grid(row=3, column=1, padx=10, pady=10, sticky="ew")

def history():
    if not os.path.exists(output_file):
        create_file = messagebox.askyesno("Create File?", f"{output_file} does not exist. Would you like to create it?")
        if create_file:
            open(output_file, 'a').close()
        else:
            return

    try:
        with open(output_file, "r") as f:
            content = f.read()
            history_window = Toplevel(w)
            history_window.title("Copy Log")
            text_area = Text(history_window, wrap=WORD, bg="white", font=('Courier New', 10))
            text_area.insert(END, content)
            text_area.pack(expand=True, fill=BOTH, padx=10, pady=10)
            text_area.update_idletasks()
            history_window.geometry(f"{text_area.winfo_reqwidth()+20}x{text_area.winfo_reqheight()+20}")
    except FileNotFoundError:
        error_window = Toplevel(w)
        error_window.title("Error")
        error_label = Label(error_window, text=f"Error: {output_file} not found.", font=('Arial', 10))
        error_label.pack(padx=20, pady=20)

history_button = tkinter.Button(w, text="Copy Logs", command=history, bg="#2196F3", fg="white", font=('Arial', 10))
history_button.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

def browse_source():
    filename = filedialog.askdirectory()
    source_value.set(filename)

def browse_destination():
    filename = filedialog.askdirectory()
    destination_value.set(filename)

source_browse_button = tkinter.Button(w, text="Browse", command=browse_source, bg="#e0e0e0", font=('Arial', 8))
source_browse_button.grid(row=0, column=2, padx=5, pady=5)

destination_browse_button = tkinter.Button(w, text="Browse", command=browse_destination, bg="#e0e0e0", font=('Arial', 8))
destination_browse_button.grid(row=1, column=2, padx=5, pady=5)

w.grid_columnconfigure(1, weight=1)

def on_closing():
    if messagebox.askokcancel("Quit", "Are you sure you want to quit? Upon closing the program will be removed."):
        destroy_self()
        w.destroy()

w.protocol("WM_DELETE_WINDOW", on_closing)

w.mainloop()