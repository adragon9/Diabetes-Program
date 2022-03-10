def correction_calculator(blood_sugar, target=None, correction_factor=None):
    # formula for the calculator personal to each person have to change
    correction = (blood_sugar - target) / correction_factor

# if the blood sugar is higher than target print correction else print no correction
    if blood_sugar <= target:
        # print("No correction") -- debug print
        return "No correction"
    else:
        # print("Your correction is -->", correction) -- debug print
        return str(correction)
