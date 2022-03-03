from tkinter import Button, Label
from os.path import exists

from Dependencies import Windows
from Dependencies.Calculators import correction_calculator

def letter_scrub(text):
    index = 0
    for i in text:
        if not i.isnumeric():
            text = text.replace(i, '')
        else:
            # print("--> n") # Debug print
            index += 1
    return text

# submit button function
def submit():
    # Filters out anything that is not a number
    bsEntry = Windows.Window1.bsEntry
    mealEntry = Windows.Window1.mealEntry
    doseEntry = Windows.Window1.doseEntry

    if bsEntry is not None:
        cleanBsEntry = letter_scrub(bsEntry.get())

    if mealEntry is not None:
        cleanMealEntry = letter_scrub(mealEntry.get())

    if doseEntry is not None:
        cleanDoseEntry = letter_scrub(doseEntry.get())

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

    fileName = "Test.txt"
    char = " "
    if not exists("Test.txt"):
        with open(fileName, 'w') as logFile:
            logFile.write("Blood sugar"+char*(20 - len("blood sugar"))+"Meal"+char*(20-len("Meal"))+"Dose\n"+
                          "{}".format(cleanBsEntry)+char*(20 - len(cleanBsEntry))+"{}".format(cleanMealEntry)+char*(20-len(cleanMealEntry))+"{}\n".format(cleanDoseEntry))
    else:
        with open(fileName, 'a') as logFile:
            logFile.write("{}".format(cleanBsEntry)+char*(20 - len(cleanBsEntry))+"{}".format(cleanMealEntry)+char*(20-len(cleanMealEntry))+"{}\n".format(cleanDoseEntry))