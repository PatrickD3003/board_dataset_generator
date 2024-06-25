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

    2. Generate level 1,2,3 itemsets:
       Containing all the holds used in V{i} as key, and its total appearance(candidate support count) as value.
       Compare the candidate support count with minimum support count, remove if its smaller than the minimum support count.
       ex (holds data on V3)
       L1 = {'A1': 2, 'A2': 1,'A3': 4}
       minimum support count = 2, remove 'A2'.
    """
    def __init__(self, grade: str):
        self.lowest_grade = 3
        self.highest_grade = 10
        self.raw_data = get_data_from_database(grade)
        self.min_support_count = 2
    
    def get_raw_data(self):
        return self.raw_data
    
    def convert(self, string: str) -> list:
        """
        function to convert a string into a list with
        comma separated. 
        """
        li = list(string.split(","))
        return li
    
    def process_raw_data(self) -> list:
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
    
    def get_processed_data(self) -> list:
        return self.process_raw_data()
    
    def flatten_list(self, data: list) -> list:
        """
        function that get a 2D list of processed_data,
        turns it into a 1D list containing only all the holds.
        """
        return [holds for problem in data for holds in problem[1]]
    
    def extract_unique_element(self, l_data_keys: list) -> list:
        """
        generate aa list of unique elements from a list of tuples(or lists) of data keys.
        """
        unique_element = []
        for tuple_data in l_data_keys:
            for element in tuple_data:
                if element not in unique_element:
                    unique_element.append(element)
        return unique_element
    
    def create_combination(self, l_data: dict) -> list:
        """
        function to create combination of two itemset data.
        make sure its not doubled
        ex: (A1, A3), (A3, A1) is considered the same.
        """
        l_data_keys = [set(key) for key in l_data]
        unique_element = self.extract_unique_element(l_data_keys)
        combination_data = []
        for l_data_set in l_data_keys:
            for element in unique_element:
                # create a new combined set
                combined_set = set(l_data_set)
                combined_set.add(element)
                if (len(combined_set) == len(l_data_set) + 1) and (combined_set not in combination_data):
                    combination_data.append(combined_set)
        # turn it into tuple again
        combination_data = [tuple(data) for data in combination_data]
        return combination_data
    
    def compare_with_minimum_support_count(self, l_data:dict) -> dict:
        """
        compare the candidate support count with the minimum support count.
        remove from the list if its < minimum support count.
        """
        return {key:l_data[key] for key in l_data if l_data[key] > self.min_support_count}
    
    def scan_D(self, data:list, c_data:list) -> dict:
        l_data = {key:0 for key in c_data}
        # scan D for count of each candidate
        for problem in data:  # iterate every problem in the data
            used_holds = problem[1]  # the first index is the holds list
            # use simple membership check method to check if all elements of c2_data are present in the used holds
            for combination in c_data:
                if all(elem in used_holds for elem in combination):
                    l_data[combination] += 1
        # remove the data with candidate support count lower than the minimum support count
        l_data = self.compare_with_minimum_support_count(l_data)
        return l_data
    
    def get_l1(self, flattened_data: list) -> dict:
        """
        get l1 itemset.
        """
        # count how many times a hold appear in the list, remove if its smaller than minimum support count
        c1_data = flattened_data
        l1_data = {tuple([key]):flattened_data.count(key) for key in flattened_data if flattened_data.count(key) > self.min_support_count}
        return l1_data
    
    def get_l2(self, processed_data: list, l1_data: list) -> dict:
        """
        get l2 itemset
        """
        # generate C2 candidates from L1
        c2_data = self.create_combination(l1_data)
        # scan D for count of each candidate, get the L2 data.
        l2_data = self.scan_D(processed_data, c2_data)
        return l2_data
    
    def get_l3(self, data: list, l2_data: list) -> dict:
        """
        get l3 itemset
        """
        # generate C3 candidates from L2
        c3_data = self.create_combination(l2_data)
        # scan D for count of each candidate, get the L2 data.
        l3_data = self.scan_D(data, c3_data)
        return l3_data
    
    def get_l4(self, data, l3_data) -> dict:
        """
        get l3 itemset
        """
        # generate C3 candidates from L2
        c4_data = self.create_combination(l3_data)
        # scan D for count of each candidate, get the L2 data.
        l4_data = self.scan_D(data, c4_data)
        return l4_data

    def apriori(self) -> dict:
        """
        Apply the Apriori algorithm to find frequent itemsets.
        Returns a dictionary where each key is a grade (e.g., 'V3') and each value
        is a dictionary representing frequent itemsets at different levels.
        """
        processed_data = self.get_processed_data()
        flattened_list = self.flatten_list(processed_data)
        # create L1 combination
        l1_data = self.get_l1(flattened_list)
        # create L2 combination
        l2_data = self.get_l2(processed_data, l1_data)
        # create l3 combination
        l3_data = self.get_l3(processed_data, l2_data)
        # create l4 combination
        l4_data = self.get_l4(processed_data, l3_data)
        return l4_data
    
def analyze_with_apriori() -> dict:
    """
    summarize the datas gained from apriori algorithm.
    """
    lowest_grade = 3
    highest_grade = 10
    summarize_data = dict()
    for grade in range(lowest_grade, highest_grade + 1):
        grade = f"V{grade}"
        apri = Apriori(grade)
        apri_data = apri.apriori()
        summarize_data[grade] = apri_data

    return summarize_data


if __name__ == "__main__":
    analysis = analyze_with_apriori()
    for key in analysis:
        print(f"grade: {key}, result {analysis[key]}")