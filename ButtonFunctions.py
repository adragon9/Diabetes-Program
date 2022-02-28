from tkinter import *
from os.path import exists

import Windows
from Calculators import correction_calculator


# submit button function
def submit_bs():
    # Filters out anything that is not a number
    index = 0
    for i in Windows.Window1.bsEntry.get():
        if not i.isnumeric():
            Windows.Window1.bsEntry.delete(index)
        else:
            # print("--> n") # Debug print
            index += 1

    # No reason to read anything higher than 3 digits as that would mean you are in the hospital
    # Gives confirmation of success and lets the user know if the input is wrong
    bsEntry = Windows.Window1.bsEntry
    root = Windows.Window1.root
    warningLabel = Label(root)

    if 3 >= len(bsEntry.get()) > 0:
        warningLabel['foreground'] = "green"
        warningLabel['text'] = "Submitted"
        warningLabel.grid(row=1, column=2)
        warningLabel.after(5000, warningLabel.destroy)
        print(bsEntry.get())  # debug print used until file writing was set up
        correction_calculator(int(bsEntry.get()))
    else:
        warningLabel['foreground'] = "red"
        warningLabel['text'] = "Entry Invalid"
        warningLabel.grid(row=1, column=2)
        warningLabel.after(5000, warningLabel.destroy)
        bsEntry.delete(0, len(bsEntry.get()))
        print("Value out of range")

    fileName = "Test.txt"
    if not exists("Test.txt"):
        with open(fileName, 'w') as logFile:
            logFile.write("TEST\n{}\n".format(bsEntry.get()))
    else:
        with open(fileName, 'a') as logFile:
            logFile.write("{}\n".format(bsEntry.get()))
