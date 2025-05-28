# Torreno, Lerrica Jeremy S. 
# BSCS-DS 2 | DAA
# counting algo 

# Create a working program that will count the number of males, females and computers in this computer lab
#from flask import Flask, render_template, request

#app = Flask(__name__)

# Your dataset
def get_counts():
    dataStudent = ["male", "male", "male", "male", "male", "male", "male", "male", "male", "male", "male",
                "Female", "female", "female", "female", "female", "female"]
    dataLab = ["computer", "Computer", "computer", "computer", "computer", "computer", "computer", "computer",
            "computer", "computer", "computer", "computer", "computer", "computer", "computer", "computer",
            "computer", "computer", "computer", "computer"] 
    
    males = sum(1 for s in dataStudent if s.lower() == 'male')
    females = sum(1 for s in dataStudent if s.lower() == 'female')
    computers = sum(1 for item in dataLab if item.lower() == 'computer')
    return {
        'males': males,
        'females': females,
        'computers': computers,
        'students': dataStudent,
        'lab': dataLab
    }
