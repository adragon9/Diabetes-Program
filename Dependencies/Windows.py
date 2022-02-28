from tkinter import *

from Dependencies.ButtonFunctions import submit_bs


class Window1:
    # Window setup
    root = Tk()
    root.geometry("500x500")
    root.wm_title("Diabetes Logbook")

    # Blood sugar entry label and entry box
    bsLabel = Label(root, text="Blood Sugar")
    mealLabel = Label(root, text="Meal Carbs")
    doseLabel = Label(root, text="Dose")
    bsEntry = Entry(root)
    mealEntry = Entry(root)
    doseEntry = Entry(root)

    submitBsButton = Button(root, text="Submit", command=submit_bs)  # submit button
    submitMealButton = Button(root, text="Submit")
    submitDoseButton = Button(root, text="Submit")


def window_1_layout():
    # Widget positioning
    Window1.bsLabel.grid(row=0, column=0)
    Window1.mealLabel.grid(row=2, column=0)
    Window1.doseLabel.grid(row=4, column=0)
    Window1.bsEntry.grid(row=1, column=0)
    Window1.mealEntry.grid(row=3, column=0)
    Window1.doseEntry.grid(row=5, column=0)
    Window1.submitBsButton.grid(row=1, column=1)
    Window1.submitMealButton.grid(row=3, column=1)
    Window1.submitDoseButton.grid(row=5, column=1)
