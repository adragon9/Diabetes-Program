from tkinter import *
import CorrectionCalculator as cCalc


# submit button function
def submit():
    # Filters out anything that is not a number
    index = 0
    for i in bsEntry.get():
        if not i.isnumeric():
            bsEntry.delete(index)
        else:
            # print("--> n") # Debug print
            index += 1

    # No reason to read anything higher than 3 digits as that would mean you are in the hospital
    # Gives confirmation of success and lets the user know if the input is wrong
    warningLabel = Label(root)
    if 3 >= len(bsEntry.get()) > 0:
        warningLabel['foreground'] = "green"
        warningLabel['text'] = "Submitted"
        warningLabel.grid(row=2, column=0)
        warningLabel.after(5000, warningLabel.destroy)
        print(bsEntry.get())  # debug print used until file writing was set up
        cCalc.correction_calculator(int(bsEntry.get()))
    else:
        warningLabel['foreground'] = "red"
        warningLabel['text'] = "Entry Invalid"
        warningLabel.grid(row=2, column=0)
        warningLabel.after(5000, warningLabel.destroy)
        bsEntry.delete(0, len(bsEntry.get()))
        print("Value out of range")


# Main script
if __name__ == "__main__":
    # Window setup
    root = Tk()
    root.geometry("500x500")
    root.wm_title("Diabetes Logbook")

    # Blood sugar entry label and entry box
    bsLabel = Label(root, text="Blood Sugar")
    bsEntry = Entry(root)

    submitButton = Button(root, text="Submit", command=submit)  # submit button

    # Widget positioning
    bsLabel.grid(row=0, column=0)
    bsEntry.grid(row=1, column=0)
    submitButton.grid(row=1, column=1)

    mainloop()

