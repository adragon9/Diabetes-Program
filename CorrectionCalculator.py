def correction_calculator(blood_sugar):

    correction = (blood_sugar - 120) / 20

    if blood_sugar <= 120:
        print("No Correction")
    else:
        print("Your correction is -->", correction)
