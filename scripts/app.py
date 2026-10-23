import bmi

result = bmi.compute_bmi(70, 1.75)
print(f"Your BMI is {result:.2f}, and your category is {bmi.classify_bmi(result)}.")
#