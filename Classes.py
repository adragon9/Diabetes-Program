import tkinter as tk

"""
File: Classes.py
Contains entry box objects for easier implementation and access
"""


class EntryBox(tk.Tk):
    """
    Allows for one to make an entry box by inserting the master window, width, grid row, and grid column
    """
    def __init__(self, master=None, width=None, row=None, column=None):
        self.entryBox = None
        self.master = master
        self.width = width
        self.row = row
        self.column = column

    def initialize_box(self):
        """
        initialize_box() Initializes the entry box by calling tk's entry box function, and grid function
        """
        self.entryBox = tk.Entry(self.master, width=self.width)
        self.entryBox.grid(row=self.row, column=self.column)

    def get_box(self):
        """
        get_data() the entry box for easy access
        """
        # print(self.entryBox.get()) -- debug print
        return self.entryBox


class CustButton(tk.Tk):
    """
    Allows for easy creation of a button accepts:
    master window, text of the button, width of the button, its grid row and column, the buttons callback command,
    and the buttons padx and pady
    """
    def __init__(self, master=None, text=None, width=None, row=None, column=None, command=None, padx=None, pady=None):
        self.button = None
        self.master = master
        self.text = text
        self.width = width
        self.row = row
        self.column = column
        self.padx = padx
        self.pady = pady
        self.command = command

    def initialize_button(self):
        """
        initialize_button: initializes the button with the passed values
        """
        self.button = tk.Button(self.master, text=self.text, width=self.width, command=self.command)
        self.button.grid(row=self.row, column=self.column, padx=self.padx, pady=self.pady)
