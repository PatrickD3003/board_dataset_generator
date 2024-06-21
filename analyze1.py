from database.database import get_data_from_database
import matplotlib.pyplot as plt
import numpy as np


"""
goal:
to analyze the relationship between the holds used and the grade's difficulty level.
input: 
2D list of label, each element containing one benchmark problem's used holds.
for example, 
V3 = [["A1","A2", "K18", etc], ["J18", "J7", "B18", etc], [etc]]
V4 = [["A3","A4", "K16", etc], ["J18", "J9", "B18", etc], [etc]]
etc

output:
graph that shows how much a holds appears on each grade.

for example, (make a graph out of this)

label = "A1"
"A1" appears on V3 problem 5 times,
"A1" appears on V4 problem 2 times,
"A1" appears on V5 problem 7 times, 
etc

label = "A2"
"A2" appears on V3 problem 1 times,
"A2" appears on V4 problem 0 times,
"A2" appears on V5 problem 11 times, 
"""

def holds_dictionary_generator():
    """
    create a dictionary containing hold label as key and its quantity as value.
    all quantity is set to 0 in the beginning.
    """
    holds_dictionary = dict()
    alphabets = "ABCDEFGHIJK"

    for alphabet in alphabets:
        for i in range(1, 19):
            label = alphabet + f"{i}"
            holds_dictionary[label] = {"V3":0, "V4":0, "V5":0, 
                                       "V6":0, "V7":0, "V8":0,"V9":0, "V10":0}
    return holds_dictionary

def get_holds_list(grade):
    """
    return a 1 dimension list of all the holds used in a particular grade benchmark.
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
    return all_holds

def input_data_to_dictionary():
    # get the grade range. starts at V3 and ends at V10
    lowest_grade = 3
    highest_grade = 10
    # create the dictionary of holds.
    holds_dict = holds_dictionary_generator()

    for grade in range(lowest_grade, highest_grade):
        # analyze each grade
        # create a hold dictionary to count its appearance frequency
        grade = f"V{grade}"
        appeared_holds = get_holds_list(grade)
        for hold in appeared_holds:
            selected_holds = holds_dict[hold]
            selected_holds[grade] += 1

    return holds_dict

def create_graph(holds_dict):
    # iterate through the dictionary
    for key in holds_dict:
        fig, ax = plt.subplots()
        label_name = key
        xy_value = holds_dict[key]
        x_value = [key for key in xy_value]
        y_value = [xy_value[key] for key in xy_value]
        ax.bar(x_value, y_value)
        ax.set_yticks(range(0, 20))
        fig.savefig(f"analyze/{label_name}.PNG")


holds_dictionary = input_data_to_dictionary()
create_graph(holds_dictionary)``