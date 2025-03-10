import os
import sys
import tkinter
from tkinter import *
import datetime

w = tkinter.Tk()
w.geometry("300x200")
w.title("Copy Assistant")

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

    with open(output_file, "a") as f:  # Open in append mode
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

        sys.stdout = original_stdout  # Restore standard output


clicked = StringVar()
clicked.set("local")
drop = OptionMenu(w, clicked, "Local", "Network")
source_label = tkinter.Label(w, text='Source:')
source_entry = tkinter.Entry(w, textvariable=source_value, font=('calibre', 10, 'normal'))
destination_label = tkinter.Label(w, text='Destination:', font=('calibre', 10, 'bold'))
destination_entry = tkinter.Entry(w, textvariable=destination_value, font=('calibre', 10, 'normal'))

sub_btn = tkinter.Button(w, text='Submit', command=submit)
source_label.grid(row=0, column=0)
source_entry.grid(row=0, column=1)
destination_label.grid(row=1, column=0)
destination_entry.grid(row=1, column=1)
drop.grid(row=2, column=1)
sub_btn.grid(row=3, column=1)


def history():
    try:
        with open(output_file, "r") as f:
            content = f.read()
            history_window = Toplevel(w)
            history_window.title("Copy Log")
            text_area = Text(history_window)
            text_area.insert(END, content)
            text_area.pack()
    except FileNotFoundError:
        print(f"Error: {output_file} not found."+" "+str(datetime.time()))


history_button = tkinter.Button(w, text="Copy Logs", command=history)
history_button.grid(row=4, column=1)

w.mainloop()
