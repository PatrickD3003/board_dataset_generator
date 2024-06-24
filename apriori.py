from database.database import get_data_from_database
import matplotlib.pyplot as plt
import numpy as np


class Apriori:
    """
    Implement the Apriori algorithm for pattern mining. The goal is to
    find out the hold combinations that appears the most on a certain grade.
    steps

    1. get the raw data containing dictionary with V{i} grade as key,
       and all the problems listed in V{i} database as value in tuple.
       ex (the real data starts at V3 until V10)
       {'V3' : [ (problem1_name, "hold1,hold2,hold3", "hold4,hold5", "hold6"), (problem2_name, "hold1,hold2,hold3", "hold4,hold5", "hold6"), (problem3_name, "hold1,hold2,hold3", "hold4,hold5", "hold6") ], 
        'V4' : [ (problem1_name, "hold1,hold2,hold3", "hold4,hold5", "hold6"), (problem2_name, "hold1,hold2,hold3", "hold4,hold5", "hold6"), (problem3_name, "hold1,hold2,hold3", "hold4,hold5", "hold6") ] 
        etc }

    2. make a new dictionary:
       containing all the holds used in V{i} as key, and its total appearance as value
       ex (holds data on V3)
       L1 = {'A1': 2, 'A2': 1,'A3': 4}
    """
    def __init__(self, grade):
        self.lowest_grade = 3
        self.highest_grade = 10
        self.raw_data = get_data_from_database(grade)
        self.min_support_count = 4
    
    def get_raw_data(self):
        return self.raw_data
    
    def convert(self, string):
        """
        function to convert a string into a list with
        comma separated. 
        """
        li = list(string.split(","))
        return li
    
    def process_raw_data(self):
        """
        turn the raw data into a more usable form.
        ex : 
        from ('STARLIGHT', 'H18', 'G13,D14,B10,C6', 'A2') 
        into ('STARLIGHT', ['H18', 'G13', 'D14', etc])
        """
        processed_data = []
        for problem in self.raw_data:
            problem_name = problem[0]
            goal_hold = self.convert(problem[1])
            middle_hold = self.convert(problem[2])
            start_hold = self.convert(problem[3])
            all_holds = goal_hold + middle_hold + start_hold
            processed_data.append((problem_name, all_holds))
        return processed_data
    
    def get_processed_data(self):
        return self.process_raw_data()
    
    def flatten_list(self, data):
        """
        function that get a 2D list of processed_data,
        turns it into a 1D list containing only all the holds.
        """
        return [holds for problem in data for holds in problem[1]]
    
    def create_combination(self, data1, data2):
        """
        function to create combination of two itemset data.
        make sure its not doubled
        ex: (A1, A3), (A3, A1) is considered the same.
        """
        data1 = [key for key in data1]
        data2 = [key for key in data2]
        None

    def get_l1(self, data):
        """
        function to get l1 itemset.
        """
        # count how many times a hold appear in the list, remove if its smaller than minimum support count
        l1_data = {key:data.count(key) for key in data if data.count(key) > self.min_support_count}
        return l1_data
    
    def get_l2(self, data, l1_data):
        """
        function to get l2 itemset
        """

        None

    def apriori(self):
        processed_data = self.get_processed_data()
        all_holds_list = self.flatten_list(processed_data)
        # create L1 combination
        l1_data = self.get_l1(all_holds_list)
        # create L2 combination
        l2_data = self.get_l2(processed_data, l1_data)

if __name__ == "__main__":
    apri = Apriori("V3")
    apri_data = apri.apriori()
    print(apri_data)