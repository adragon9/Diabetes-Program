import tkinter as tk
import Classes
import datetime

from os.path import exists
from os import getcwd
from PIL import Image, ImageTk
from Calculators import correction_calculator


# Version 2.0
# Last revision 3/10/2022


# noinspection PyGlobalUndefined
def setting_window():
    # Sets up a settings file that stores blood sugar target and correction factor for correction calculation
    def setting_submit():
        target = targetBS.get_box()
        cfactor = correctionFactor.get_box()

        target = letter_scrub(target)
        cfactor = letter_scrub(cfactor)

        # if there is no value, the target is set to 120 and the correction factor is set to 20
        if target is None:
            target = 120
        if cfactor is None:
            cfactor = 20

        # Writes to a setting file
        with open('Settings.dat', 'w') as file:
            file.write("{}\n".format(target))
            file.write("{}\n".format(cfactor))

    window = tk.Toplevel(root)
    window.geometry("1200x720")
    window.title("Settings")
    window.grab_set()

    global settingsImage
    # Side image set up
    settingsImage = Image.open("{}\\Resources\\download (2).png".format(getcwd()))
    settingsImage = settingsImage.resize((360, 1200))
    settingsImage = ImageTk.PhotoImage(settingsImage)

    # Image setup
    settingsImageLabel = tk.Label(window, image=settingsImage)
    settingsImageLabel.grid(rowspan=30, column=0)

    # Window column configuration
    window.columnconfigure(0)
    window.columnconfigure(3, weight=1)

    # Window row configuration
    window.rowconfigure(0, weight=1)
    window.rowconfigure(3, weight=1)
    # Create Labels
    targetLabel = tk.Label(window, text="Target Blood Sugar", font=("Times New Roman", 12), width=15, justify='right',
                           anchor="e")
    correctionFactorLabel = tk.Label(window, text="Correction Factor", font=("Times New Roman", 12), width=15,
                                     justify='right', anchor="e")

    targetLabel.grid(row=1, column=1)
    correctionFactorLabel.grid(row=2, column=1)

    # Create entry boxes
    targetBS = Classes.EntryBox(window, 30, 1, 2)
    correctionFactor = Classes.EntryBox(window, 30, 2, 2)
    targetBS.initialize_box()
    correctionFactor.initialize_box()

    subButton = Classes.CustButton(window, "Submit >", 12, 4, 4, setting_submit, padx=5, pady=5)
    subButton.initialize_button()


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
    return text  # returns the scrubbed text


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
    bsEntry = bsBox.get_box()
    mealEntry = mealBox.get_box()
    doseEntry = doseBox.get_box()
    cleanBsEntry = ""
    cleanMealEntry = ""
    cleanDoseEntry = ""
    # places the entry box data into a list for convenience
    entryBoxData = [bsEntry, mealEntry, doseEntry]
    # ensures letter_scrub doesn't run without input
    if bsEntry is not None:
        # wanted to preserve the raw entry box data so that I could manipulate the entry box
        cleanBsEntry = letter_scrub(entryBoxData[0].get())

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
    invalidEntry = bool
    global warningLabel
    global warningText
    global correctionLabel
    global correctionText
    setting_value = ['', '']

    # Get the correction using the user settings
    with open("Settings.dat", 'r') as file:
        index = 0
        a = file.read().split()
        for line in a:
            setting_value[index] = line
            # print(setting_value[index2]) -- debug print
            # print(index2) -- debug print
            index += 1

    correction = correction_calculator(int(cleanBsEntry), target=int(setting_value[0]),
                                       correction_factor=int(setting_value[1]))

    index = 0
    if cleanBsEntry != '':
        for i in entryBoxData:
            # print(i) -- debug print
            if len(i.get()) > 4:
                invalidEntry = True
                warningLabel.config(foreground='red')
                warningText.set("Error {} is invalid; detected in {}".format(i.get(), get_entry_name(index)))
                i.delete(0, len(i.get()))
                # print("Value out of range") -- debug print
                break
            else:
                invalidEntry = False
                warningLabel.config(foreground='green')
                warningText.set("Submitted")
                # print(cleanBsEntry) -- debug print
                correctionLabel.config(relief='groove', padx=10, pady=10, background="#EEEE9B")
                correctionText.set("Your correction is: {}".format(correction))
            index += 1
    else:
        invalidEntry = True
        warningLabel.config(foreground='red')
        warningText.set("Error no Blood Sugar entered.")
        entryBoxData[0].delete(0, len(entryBoxData[0].get()))
        # print("Value out of range") -- debug print

    # Writes to the file
    fileName = "DiabetesLog.txt"
    char = " "  # variable used for spacing in the txt file
    currentTime = datetime.datetime.now()
    timeStamp = currentTime.strftime("%d/%m/%Y %H:%M:%S %p")
    # Does not write invalid entries to file

    if invalidEntry is False:
        # if the file doesn't exist it opens as write else opens as append
        if not exists("DiabetesLog.txt"):
            with open(fileName, 'w') as logFile:
                # File output and formatting
                # Formatted for best the possible readability I could get
                logFile.write("Time/Date" + char * (30 - len("Time/Date")) +
                              "Blood sugar" + char * (30 - len("blood sugar")) +
                              "Meal" + char * (30 - len("Meal")) +
                              "Dose" + char * (30 - len("Dose")) +
                              "Correction\n" +
                              "{}".format(timeStamp) + char * (30 - len(timeStamp)) +
                              "{}".format(cleanBsEntry) + char * (30 - len(cleanBsEntry)) +
                              "{}".format(cleanMealEntry) + char * (30 - len(cleanMealEntry)) +
                              "{}".format(cleanDoseEntry) + char * (30 - len(cleanDoseEntry)) +
                              "{}\n".format(correction))
        else:
            with open(fileName, 'a') as logFile:
                logFile.write("{}".format(timeStamp) + char * (30 - len(timeStamp)) +
                              "{}".format(cleanBsEntry) + char * (30 - len(cleanBsEntry)) +
                              "{}".format(cleanMealEntry) + char * (30 - len(cleanMealEntry)) +
                              "{}".format(cleanDoseEntry) + char * (30 - len(cleanDoseEntry)) +
                              "{}\n".format(correction))  # file formatting


# Main
if __name__ == "__main__":
    # creates the settings file if it doesn't exist
    if not exists("Settings.dat"):
        with open("Settings.dat", 'w') as settings:
            settings.write("120\n20")

    root = tk.Tk()
    root.geometry("1200x720")
    root.title("Logbook")

    sideImage = Image.open("{}\\Resources\\download.png".format(getcwd()))
    sideImage = sideImage.resize((360, 1200))
    sideImage = ImageTk.PhotoImage(sideImage)

    # Image setup
    imageLabel = tk.Label(root, image=sideImage)
    imageLabel.grid(rowspan=30, column=0)

    # Column Configuration
    root.grid_columnconfigure(0)
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(4, weight=3)

    # Row Configuration
    root.grid_rowconfigure(0, weight=1)
    root.grid_rowconfigure(6, weight=1)

    # Label Vars
    warningText = tk.StringVar()
    correctionText = tk.StringVar()

    # Labels setup
    warningLabel = tk.Label(root, textvariable=warningText, anchor='center')
    correctionLabel = tk.Label(root, textvariable=correctionText, anchor='center')
    headerLabel = tk.Label(root, text="Diabetes Log", font=("Times New Roman", 36), width=15, anchor='w')
    bsLabel = tk.Label(root, text="Blood Sugar", font=("Times New Roman", 12), width=15, justify='right', anchor="e")
    mealLabel = tk.Label(root, text="Meal Carbs", font=("Times New Roman", 12), width=15, justify='right', anchor="e")
    doseLabel = tk.Label(root, text="Dose", font=("Times New Roman", 12), width=15, justify='right', anchor="e")

    warningLabel.grid(row=4, column=2, columnspan=2)
    correctionLabel.grid(row=5, column=2, columnspan=2)
    headerLabel.grid(row=0, column=1, columnspan=10, sticky='w')
    bsLabel.grid(row=1, column=2)
    mealLabel.grid(row=2, column=2)
    doseLabel.grid(row=3, column=2)

    # Created boxes as classes to collect and use their data elsewhere as needed
    bsBox = Classes.EntryBox(root, 30, 1, 3)
    mealBox = Classes.EntryBox(root, 30, 2, 3)
    doseBox = Classes.EntryBox(root, 30, 3, 3)
    bsBox.initialize_box()
    mealBox.initialize_box()
    doseBox.initialize_box()

    submit = Classes.CustButton(root, "Submit >", 12, 8, 5, submit, padx=50, pady=25)
    settings = Classes.CustButton(root, "Settings", 12, 7, 5, setting_window, padx=50)
    submit.initialize_button()
    settings.initialize_button()

    root.mainloop()
