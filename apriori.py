from database.database import get_data_from_database
import matplotlib.pyplot as plt
import numpy as np


class Apriori:
    """
    Implement the Apriori algorithm for pattern mining. The goal is to
    find out the hold combinations that appears the most on a certain grade.
    """
    def __init__(self):
        self.lowest_grade = 3
        self.highest_grade = 10
        self.raw_data = {f"V{grade}": get_data_from_database(f"V{grade}") for grade in range(self.lowest_grade, self.highest_grade + 1)}
    
    def get_raw_data(self):
        return self.raw_data
    

apri = Apriori()
apri_raw = apri.get_raw_data()
print(apri_raw)