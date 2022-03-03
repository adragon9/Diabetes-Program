def correction_calculator(blood_sugar):

    correction = (blood_sugar - 120) / 20  # formula for the calculator personal to each person have to change

# if the blood sugar is higher than target print correction else print no correction
    if blood_sugar <= 120:
        print("No Correction")
    else:
        print("Your correction is -->", correction)
