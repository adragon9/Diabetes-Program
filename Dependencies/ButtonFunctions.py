from tkinter import Button, Label, StringVar
from os.path import exists
from Dependencies import appWindowConfig as aWC

from Dependencies.Calculators import correction_calculator

# gets the entry boxes text and scrubs any non numeric characters
def letter_scrub(text):
    index = 0
    for i in text:
        if index == 0 and i == '-':
            continue
        else:
            if not i.isnumeric():
                text = text.replace(i, '')
            else:
                # print("--> n") # Debug print
                index += 1
    return text # returns the scrubbed text

def neg_scrub(text):
    if int(text) < 0:
        return True
    else:
        return False

def get_entry_name(index):
    if index == 0:
        return "Blood Sugar Entry"
    elif index == 1:
        return "Meal Entry"
    elif index == 2:
        return "Dose Entry"
    else:
        return "Unknown"


# submit button function
def submit():
    # Filters out anything that is not a number
    bsEntry = aWC.MainWindow.bsEntry
    mealEntry = aWC.MainWindow.mealEntry
    doseEntry = aWC.MainWindow.doseEntry
    # places the entry box data into a list for convinience
    entryBoxData = [bsEntry, mealEntry, doseEntry]
    # ensures letter_scrub doesn't run without input
    if bsEntry is not None:
        cleanBsEntry = letter_scrub(entryBoxData[0].get()) # wanted to preserve the raw entry box data so that I could manipulate the entry box

    if mealEntry is not None:
        cleanMealEntry = letter_scrub(entryBoxData[1].get())

    if doseEntry is not None:
        cleanDoseEntry = letter_scrub(entryBoxData[2].get())

    # makes sure that blank entries are entered as 0
    if cleanMealEntry == '':
        cleanMealEntry = "0"

    if cleanDoseEntry == '':
        cleanDoseEntry = "0"

    # No reason to read anything higher than 3 digits as that would mean you are in the hospital
    # Gives confirmation of success and lets the user know if the input is wrong
    invalidEntry: bool
    warningLabel = aWC.MainWindow.warningLabel
    warningText = aWC.MainWindow.warningLabelText

    index = 0
    if cleanBsEntry != '':
        for i in entryBoxData:
            print(i.get())
            if len(i.get()) > 4:
                invalidEntry = True
                warningLabel.config(foreground='red')
                warningText.set("Error {} is invalid; detected in {}".format(i.get(), get_entry_name(index)))
                i.delete(0, len(i.get()))
                print("Value out of range")
                break
            else:
                correction = correction_calculator(int(cleanBsEntry))
                invalidEntry = False
                warningLabel.config(foreground='green')
                warningText.set("Submitted")
                print(cleanBsEntry)  # debug print used until file writing was set up
                aWC.MainWindow.correctionLabel.config(background="grey")
                aWC.MainWindow.correctionText.set("Your correction is: {:0.2f}".format(float(correction)))
            index += 1
    else:
        invalidEntry = True
        warningLabel.config(foreground='red')
        warningText.set("Error no Blood Sugar entered.")
        entryBoxData[0].delete(0, len(entryBoxData[0].get()))
        print("Value out of range")

    # Writes to the file
    fileName = "Test.txt"
    char = " " # variable used for spacing in the txt file
    if invalidEntry is False:
        if not exists("Test.txt"): # if the file doesn't exist it opens as write else opens as MainWindowend
            with open(fileName, 'w') as logFile:
                logFile.write("Blood sugar"+char*(20 - len("blood sugar"))+"Meal"+char*(20-len("Meal"))+"Dose\n"+
                              "{}".format(cleanBsEntry)+char*(20 - len(cleanBsEntry))+"{}".format(cleanMealEntry)+char*(20-len(cleanMealEntry))+"{}\n".format(cleanDoseEntry)) # file formatting
        else:
            with open(fileName, 'a') as logFile:
                logFile.write("{}".format(cleanBsEntry)+char*(20 - len(cleanBsEntry))+"{}".format(cleanMealEntry)+char*(20-len(cleanMealEntry))+"{}\n".format(cleanDoseEntry)) # file formatting


def settings_submit():
    with open("Settings.dat", 'w') as configFile:
        configFile.write()
