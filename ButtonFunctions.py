from tkinter import *

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
    warningLabel = Label(Windows.Window1.root)
    if 3 >= len(Windows.Window1.bsEntry.get()) > 0:
        warningLabel['foreground'] = "green"
        warningLabel['text'] = "Submitted"
        warningLabel.grid(row=1, column=2)
        warningLabel.after(5000, warningLabel.destroy)
        print(Windows.Window1.bsEntry.get())  # debug print used until file writing was set up
        correction_calculator(int(Windows.Window1.bsEntry.get()))
    else:
        warningLabel['foreground'] = "red"
        warningLabel['text'] = "Entry Invalid"
        warningLabel.grid(row=1, column=2)
        warningLabel.after(5000, warningLabel.destroy)
        Windows.Window1.bsEntry.delete(0, len(Windows.Window1.bsEntry.get()))
        print("Value out of range")
