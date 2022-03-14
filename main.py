import datetime
import tkinter as tk
from os.path import exists

import Classes
from Calculators import correction_calculator


# Version 2.0
# Last revision 3/14/2022
global subSideImage


def setting_window():
    # Sets up a settings file that stores blood sugar target and correction factor for correction calculation
    def setting_submit():
        target = targetBS.get_box()
        cfactor = correctionFactor.get_box()

        target = letter_scrub(target.get())
        cfactor = letter_scrub(cfactor.get())

        settingsValues = [target, cfactor]
        print(settingsValues)
        # if there is no value, the target is set to 120 and the correction factor is set to 20
        for i in range(len(settingsValues)):
            if settingsValues[i] is None or settingsValues[i] == '':
                if i == 0:
                    settingsValues[i] = 120
                else:
                    settingsValues[i] = 20

        # Writes to a setting file
        with open('Settings.dat', 'w') as file:
            for i in range(len(settingsValues)):
                file.write("{}\n".format(settingsValues[i]))

    window = tk.Toplevel(root)
    window.geometry("1200x720")
    window.title("Settings")
    window.grab_set()
    global subSideImage
    # Same deal as the images in the main code
        # settingsImage = Image.open("Resources\\download (2).png")
        # resizedSettingsImage = settingsImage.resize((360, 1200))
        # settingsImage = ImageTk.PhotoImage(resizedSettingsImage)

    # Image setup
    subSideImage = tk.PhotoImage(file="Resources\\download (4).png")
    subCanvas = tk.Canvas(window, width=360, height=1200)
    subCanvas.grid(row=0, column=0, rowspan=100)
    subCanvas.create_image(0, 0, anchor='nw', image=subSideImage)

    # Window column configuration
    window.columnconfigure(1, weight=1)
    window.columnconfigure(5, weight=2)

    # Window row configuration
    window.rowconfigure(0, weight=40)
    window.rowconfigure(5, weight=40)
    window.rowconfigure(6, weight=1)
    # Create Labels
    targetLabel = tk.Label(window, text="Target Blood Sugar", font=("Times New Roman", 12), width=15, justify='right',
                           anchor="e")
    correctionFactorLabel = tk.Label(window, text="Correction Factor", font=("Times New Roman", 12), width=15,
                                     justify='right', anchor="e")
    subHeaderLabel = tk.Label(window, text="Settings", font=("Times New Roman", 36), width=15, anchor='w', pady=10)

    targetLabel.grid(row=2, column=2)
    correctionFactorLabel.grid(row=3, column=2)
    subHeaderLabel.grid(row=1, column=2, columnspan=10, sticky='w')

    # Create entry boxes
    targetBS = Classes.EntryBox(window, 30, 2, 3)
    correctionFactor = Classes.EntryBox(window, 30, 3, 3)
    targetBS.initialize_box()
    correctionFactor.initialize_box()

    # Create buttons
    closeSubWindow = Classes.CustButton(window, "[X] Close", 12, 6, 6, window.destroy, padx=25)
    subButton = Classes.CustButton(window, "Submit >", 12, 4, 3, setting_submit)
    closeSubWindow.initialize_button()
    subButton.initialize_button()


# Cleans non-numeric characters from strings
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


# Used for checking whether a number is negative
def neg_scrub(text):
    if int(text) < 0:
        return True
    else:
        return False


# Used to report which entry field is wrong for the user
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
    # Variable prep
    bsEntry = bsBox.get_box()
    mealEntry = mealBox.get_box()
    doseEntry = doseBox.get_box()
    correction = ''
    # places the entry box data into a list for convenience
    entryBoxData = [bsEntry, mealEntry, doseEntry]
    cleanEntryBoxData = ["", "", ""]

    # ensures letter_scrub doesn't run without input
    # Also preserves the raw entry box data for later use

    for i in range(0, len(cleanEntryBoxData)):
        if entryBoxData[i] is not None:
            cleanEntryBoxData[i] = letter_scrub(entryBoxData[i].get())

    # makes sure that blank entries are entered as 0
    for i in range(1, len(cleanEntryBoxData)):
        if cleanEntryBoxData[i] == '':
            cleanEntryBoxData[i] = "0"

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

    index = 0
    if cleanEntryBoxData[0] != '':
        correction = correction_calculator(int(cleanEntryBoxData[0]), target=int(setting_value[0]),
                                           correction_factor=int(setting_value[1]))
        for i in entryBoxData:
            # print(i) -- debug print
            if len(i.get()) > 3 or neg_scrub(cleanEntryBoxData[index]) is True:
                invalidEntry = True
                warningLabel.config(foreground='red')
                warningText.set("{} is invalid; error detected in: {}".format(i.get(), get_entry_name(index)))
                i.delete(0, len(i.get()))
                # print("Value out of range") -- debug print
                break
            else:
                invalidEntry = False
                warningLabel.config(foreground='green')
                warningText.set("Submitted")
                # print(cleanEntryBoxData[0) -- debug print
                correctionLabel.config(relief='groove', padx=10, pady=10, background="#EEEE9B")
                correctionText.set("Your correction is: {}".format(correction))
            index += 1
    else:
        invalidEntry = True
        warningLabel.config(foreground='red')
        warningText.set("Error: no blood sugar entered.")
        entryBoxData[0].delete(0, len(entryBoxData[0].get()))
        # print("Value out of range") -- debug print

    # Writes to the file
    fileName = "DiabetesLog.txt"
    char = " "  # variable used for spacing in the txt file
    currentTime = datetime.datetime.now()
    timeStamp = currentTime.strftime("%m/%d/%Y %H:%M:%S %p")
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
                              "{}".format(cleanEntryBoxData[0]) + char * (30 - len(cleanEntryBoxData[0])) +
                              "{}".format(cleanEntryBoxData[1]) + char * (30 - len(cleanEntryBoxData[1])) +
                              "{}".format(cleanEntryBoxData[2]) + char * (30 - len(cleanEntryBoxData[2])) +
                              "{}\n".format(correction))
        else:
            with open(fileName, 'a') as logFile:
                logFile.write("{}".format(timeStamp) + char * (30 - len(timeStamp)) +
                              "{}".format(cleanEntryBoxData[0]) + char * (30 - len(cleanEntryBoxData[0])) +
                              "{}".format(cleanEntryBoxData[1]) + char * (30 - len(cleanEntryBoxData[1])) +
                              "{}".format(cleanEntryBoxData[2]) + char * (30 - len(cleanEntryBoxData[2])) +
                              "{}\n".format(correction))  # file formatting


# Main
if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1200x720")
    root.title("Logbook")

    # creates the settings file if it doesn't exist
    if not exists("Settings.dat"):
        with open("Settings.dat", 'w') as settings:
            settings.write("120\n20")

    # Pillow Library broke the code, so I had to go with a less preferable method
    # Keeping this as a reminder to fix it if I ever revisit this project
        # Attempts to load image if the image is not found it loads text
        # sideImage = Image.open("Resources\\mainWindow.png")
        # resizedSideImage = sideImage.resize((360, 1200))
        # sideImage = ImageTk.PhotoImage(sideImage)
    # Image setup
    sideImage = tk.PhotoImage(file="Resources/download2.png")
    mainCanvas = tk.Canvas(root, width=360, height=1200)
    mainCanvas.grid(row=0, column=0, rowspan=100)
    mainCanvas.create_image(0, 0, anchor='nw', image=sideImage)

    # Column Configuration
    root.grid_columnconfigure(1, weight=1)
    root.grid_columnconfigure(5, weight=3)

    # Row Configuration
    root.grid_rowconfigure(0, weight=20)
    root.grid_rowconfigure(8, weight=30)
    root.grid_rowconfigure(10, weight=1)

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

    warningLabel.grid(row=6, column=3)
    correctionLabel.grid(row=7, column=3)
    headerLabel.grid(row=1, column=2, columnspan=10, sticky='w')
    bsLabel.grid(row=2, column=2)
    mealLabel.grid(row=3, column=2)
    doseLabel.grid(row=4, column=2)

    # Created boxes as classes to collect and use their data elsewhere as needed
    bsBox = Classes.EntryBox(root, 30, 2, 3)
    mealBox = Classes.EntryBox(root, 30, 3, 3)
    doseBox = Classes.EntryBox(root, 30, 4, 3)
    bsBox.initialize_box()
    mealBox.initialize_box()
    doseBox.initialize_box()

    # Button setup
    closeWindow = Classes.CustButton(root, "[X] Close", 12, 10, 6, root.destroy, padx=25)
    submit = Classes.CustButton(root, "Submit >", 12, 5, 3, submit)
    settings = Classes.CustButton(root, "Settings", 12, 10, 3, setting_window)
    closeWindow.initialize_button()
    submit.initialize_button()
    settings.initialize_button()

    root.mainloop()
