from tkinter import Button, Label
from os.path import exists

from Dependencies import Windows
from Dependencies.Calculators import correction_calculator

# gets the entry boxes text and scrubs any non numeric characters
def letter_scrub(text):
    index = 0
    for i in text:
        if not i.isnumeric():
            text = text.replace(i, '')
        else:
            # print("--> n") # Debug print
            index += 1
    return text # returns the scrubbed text

# submit button function
def submit():
    # Filters out anything that is not a number
    bsEntry = Windows.Window1.bsEntry
    mealEntry = Windows.Window1.mealEntry
    doseEntry = Windows.Window1.doseEntry

    # ensures letter_scrub doesn't run without input
    if bsEntry is not None:
        cleanBsEntry = letter_scrub(bsEntry.get()) # wanted to preserve the raw entry box data so that I could manipulate the entry box

    if mealEntry is not None:
        cleanMealEntry = letter_scrub(mealEntry.get())

    if doseEntry is not None:
        cleanDoseEntry = letter_scrub(doseEntry.get())

    # makes sure that blank entries are entered as 0
    if cleanMealEntry == '':
        cleanMealEntry = "0"

    if cleanDoseEntry == '':
        cleanDoseEntry = "0"

    # No reason to read anything higher than 3 digits as that would mean you are in the hospital
    # Gives confirmation of success and lets the user know if the input is wrong

    root = Windows.Window1.root
    warningLabel = Label(root)

    if 3 >= len(cleanBsEntry) > 0:
        warningLabel['foreground'] = "green"
        warningLabel['text'] = "Submitted"
        warningLabel.pack()
        warningLabel.after(5000, warningLabel.destroy)
        print(cleanBsEntry)  # debug print used until file writing was set up
        correction_calculator(int(cleanBsEntry))
    else:
        warningLabel['foreground'] = "red"
        warningLabel['text'] = "Blood Sugar Entry Invalid"
        warningLabel.pack()
        bsEntry.delete(0, len(bsEntry.get()))
        warningLabel.after(5000, warningLabel.destroy)
        print("Value out of range")

    # Writes to the file
    fileName = "Test.txt"
    char = " " # variable used for spacing in the txt file
    if not exists("Test.txt"): # if the file doesn't exist it opens as write else opens as append
        with open(fileName, 'w') as logFile:
            logFile.write("Blood sugar"+char*(20 - len("blood sugar"))+"Meal"+char*(20-len("Meal"))+"Dose\n"+
                          "{}".format(cleanBsEntry)+char*(20 - len(cleanBsEntry))+"{}".format(cleanMealEntry)+char*(20-len(cleanMealEntry))+"{}\n".format(cleanDoseEntry)) # file formatting
    else:
        with open(fileName, 'a') as logFile:
            logFile.write("{}".format(cleanBsEntry)+char*(20 - len(cleanBsEntry))+"{}".format(cleanMealEntry)+char*(20-len(cleanMealEntry))+"{}\n".format(cleanDoseEntry)) # file formatting