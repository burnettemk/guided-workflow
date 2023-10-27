import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo

# create the root window
root = tk.Tk()
root.title('Tkinter Open File Dialog')
root.resizable(False, False)
root.geometry('300x150')


def select_file():
    filetypes = (
        # ('text files', '*.txt'),
        ('application files', '*.exe'),
        ('All files', '*.*')
    )

    # Open a file
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='C:/Users/waffl',
        filetypes=filetypes)

    # Display filename
    showinfo(
        title='Selected File',
        message=filename,
    )
    
    # Open a folder
    directory = fd.askdirectory(
        title='Select directory',
        initialdir='/',
    )

    # Display folder
    showinfo(
        title='Selected directory',
        message=directory
    )


# open button
open_button = ttk.Button(
    root,
    text='Open a File',
    command=select_file
)

open_button.pack(expand=True)


def open_dialog():
    # run the application
    root.mainloop()
