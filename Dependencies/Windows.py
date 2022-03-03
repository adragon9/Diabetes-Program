from tkinter import Label, Tk, Entry, Button

from Dependencies.ButtonFunctions import submit


class Window1:
    # Window setup
    root = Tk()
    wHeight = 500
    wWidth = 500
    root.geometry("{}x{}".format(wHeight, wWidth))
    root.wm_title("Diabetes Logbook")

    # Blood sugar entry label and entry box
    bsLabel = Label(root, text="Blood Sugar")
    mealLabel = Label(root, text="Meal Carbs")
    doseLabel = Label(root, text="Dose")
    bsEntry = Entry(root)
    mealEntry = Entry(root)
    doseEntry = Entry(root)

    # Buttons
    submitButton = Button(root, text="Submit", command=submit)


def window_1_layout():
    # Widget positioning
    Window1.bsLabel.pack()
    Window1.bsEntry.pack()
    Window1.mealLabel.pack()
    Window1.mealEntry.pack()
    Window1.doseLabel.pack()
    Window1.doseEntry.pack()
    Window1.submitButton.pack()


