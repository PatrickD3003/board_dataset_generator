from database.database import get_data_from_database
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

"""
FInd out the holds combination that appears the most on a certain grade.
use pattern mining.
"""

def get_holds_list(grade):
    """
    return a list of all the holds used in a particular grade benchmark.
    """
    get_problem = get_data_from_database(grade)
    all_holds = []
    for problem in get_problem:
        length = len(problem)
        holds = problem[1::]
        holds = [hold.split(",") for hold in holds]
        all_holds += holds
    # turn the 2d list into a 1d list
    all_holds = [element for hold in all_holds for element in hold]
    return get_problem

def identify_pattern(get_problem):
    # Dictionary to count hold combinations
    hold_combinations_count = defaultdict(int)
    # Iterate through each moonboard problem
    for problem in get_problem:
        # Extract holds combinations from each problem
        holds = problem[1].split(',') + problem[2].split(',') + problem[3].split(',')
        # Sort holds to ignore order differences
        holds_sorted = ','.join(sorted(holds))
        # Count this combination
        hold_combinations_count[holds_sorted] += 1
        print(hold_combinations_count)
    # Find the most common hold combination
    most_common_combination = max(hold_combinations_count, key=hold_combinations_count.get)
    max_count = hold_combinations_count[most_common_combination]

    return most_common_combination, max_count

def analyze_data():
    # get the grade range. starts at V3 and ends at V10
    lowest_grade = 3
    highest_grade = 10

    for grade in range(lowest_grade, highest_grade+1):
        # analyze each grade
        # create a hold dictionary to count its appearance frequency
        grade = f"V{grade}"
        get_problem = get_holds_list(grade)
        most_common_combination, max_count = identify_pattern(get_problem)
        print(f"grade:{grade}")
        print(f"common combination:{most_common_combination}, max count:{max_count}")
        print()


analyze_data()