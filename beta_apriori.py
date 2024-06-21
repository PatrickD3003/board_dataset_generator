 
"""
steps.
C1
1. Set minimum support count : try 4.
2. Scan data for count of each candidate.
3. Compare candidate support count with minimum support count.

4. create 2 items combination.
repeat step 1,2,3
"""

def get_data(grade):
    return get_data_from_database(grade)

def get_holds_list(grade):
    """
    return a 1 dimension list of all the holds used in a particular grade benchmark.
    """
    get_problem = get_data_from_database(grade)
    all_holds = []
    count = 0
    for problem in get_problem:
        count += 1
        length = len(problem)
        holds = problem[1::]
        holds = [hold.split(",") for hold in holds]
        all_holds += holds
    print(f"count: {count}")
    # turn the 2d list into a 1d list
    all_holds = [element for hold in all_holds for element in hold]
    return all_holds

def count_holds(holds_list):
    holds_dict = {}
    for hold in holds_list:
        if hold not in holds_dict:
            holds_dict[hold] = 1
        else:
            holds_dict[hold] += 1
    return holds_dict

def apriori(holds_list):
    minimum_count = 4
    remove_key = []
    # iterate the holds, if the frequency of the holds are below the minimum count, add to the remove_key
    for key in holds_list:
        if holds_list[key] < minimum_count:
            remove_key.append(key)
    
    # remove the collected keys
    for key in remove_key:
        del holds_list[key]

    return holds_list
        

V3 = get_holds_list("V3")
V3_count = count_holds(V3)
V3_apriori = apriori(V3_count)
print(V3_apriori)