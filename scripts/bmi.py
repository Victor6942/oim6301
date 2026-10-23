def compute_bmi(weight, height):
     """compute the Body Mass Index (BMI) given weight in kg and height in meters"""
     bmi = weight / (height ** 2)

     return bmi


# wrrap the code in a function

def classify_bmi(bmi):
        if bmi >= 30:
            category = "Obese"
        elif bmi >= 25:
            category = "Overweight"
        elif bmi >= 18.5:
            category = "Normal"
        else:
            category = "Underweight"
        #print(category)
        return category

def main():
    weight = float(input("Enter your weight in kg: "))
    height = float(input("Enter your height in meters: "))
    bmi_value = compute_bmi(weight, height)
    result = classify_bmi(bmi_value)
    print(f"Your BMI is {bmi_value:.2f}, and your category is {result}.")



main()
