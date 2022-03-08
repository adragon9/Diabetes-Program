import tkinter as tk
from Dependencies.ButtonFunctions import submit


def open_sub_window():
    sub_window = tk.Toplevel(MainWindow.root)
    button = tk.Button(sub_window, text='Close', width=30)
    button.grid(row=1, column=1)


class MainWindow:
    root = tk.Tk()
    # Window setup
    root.geometry('1200x720')
    root.title('test')

    # variable declaration
    warningLabelText = tk.StringVar()
    correctionText = tk.StringVar()

    # entry setup
    bsEntry = tk.Entry(root, width=30)
    mealEntry = tk.Entry(root, width=30)
    doseEntry = tk.Entry(root, width=30)

    # label setup
    bsLabel = tk.Label(root, text="Blood Sugar", width=10, anchor='w', justify='left')
    mealLabel = tk.Label(root, text="Meal Carbs", width=10, anchor='w', justify='left')
    doseLabel = tk.Label(root, text="Insulin Dose", width=10, anchor='w', justify='left')
    correctionLabel = tk.Label(root, textvariable=correctionText, width=30)
    warningLabel = tk.Label(root, textvariable=warningLabelText, width=30)

    # button setup
    button = tk.Button(root, text='Submit >', width=12, command=submit)

    # grid formatting
    root.rowconfigure(5, weight=1)
    root.columnconfigure(4, weight=1)

    bsLabel.grid(row=1, column=1)
    bsEntry.grid(row=1, column=2)
    correctionLabel.grid(row=1, column=3)
    mealLabel.grid(row=2, column=1)
    mealEntry.grid(row=2, column=2)
    doseLabel.grid(row=3, column=1)
    doseEntry.grid(row=3, column=2)
    warningLabel.grid(row=4, column=2)
    button.grid(row=6, column=5, padx=5, pady=5)

