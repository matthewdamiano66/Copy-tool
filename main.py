import os
import sys
import tkinter
from tkinter import *
from tkinter import filedialog
import datetime
from tkinter import messagebox

w = tkinter.Tk()
w.geometry("400x250")
w.title("Copy Assistant")
w.resizable(False, False)

w.configure(bg="#f0f0f0")

source_value = tkinter.StringVar()
destination_value = tkinter.StringVar()
output_file = "history.txt"
current_time = str(datetime.datetime.now())

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

    with open(output_file, "a") as f:
        original_stdout = sys.stdout
        sys.stdout = f

        if clicked_value.lower() == "local":
            print("local")
            print(source)
            print(destination)
            print(current_time)
            command = str(header_x + " " + source + " " + destination + " " + xflags)
            os.system(command=command)
        elif clicked_value.lower() == "network":
            print("Network")
            print(source)
            print(destination)
            command = str(header_r + " " + source + " " + destination + " " + rflags)
            os.system(command)
        else:
            print("Invalid selection.")

        sys.stdout = original_stdout

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
    try:
        with open(output_file, "r") as f:
            content = f.read()
            history_window = Toplevel(w)
            history_window.title("Copy Log")
            history_window.geometry("500x400")
            text_area = Text(history_window, wrap=WORD, bg="white", font=('Courier New', 10))
            text_area.insert(END, content)
            text_area.pack(expand=True, fill=BOTH, padx=10, pady=10)
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

w.mainloop()
