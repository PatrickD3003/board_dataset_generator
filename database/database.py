import sqlite3

def data_to_database(problem_name, red, blue, green, grade):
    """
    collect all important datas and store it in SQLite file.
    including the boulder's name, grade, and the holds used on the boulder.
    input examples:
    problem_name = ['11D', '7C/V9']
    red = ['B18']
    blue = ['A5', 'F12', 'D11', 'K7', 'G8', 'K12']
    green = ['J3', 'E4']
    """
    connect_sql = sqlite3.connect('database/boards.db')
    cursor = connect_sql.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {grade}
                    (name TEXT PRIMARY KEY, grade TEXT, goal TEXT, middle TEXT, start TEXT) ''')
    
    # prepare data to be inserted
    name = problem_name[0]
    problem_grade = problem_name[1]
    # convert list to a comma-separated string
    goal = ','.join(red)  
    middle = ','.join(blue) 
    start = ','.join(green) 

    # insert the data into the table
    cursor.execute(f'''INSERT OR REPLACE INTO {grade} (name, grade, goal, middle, start)
                   VALUES(?, ?, ?, ?, ?)''', (name, problem_grade, goal, middle, start))
    # commit the transaction and close the connection
    connect_sql.commit()
    connect_sql.close()


def get_data_from_database(table_name):
    """
    a function to fetch data from table in database.
    """
    # open connection
    connect_sql = sqlite3.connect('database/boards.db')
    # open cursor
    cursor = connect_sql.cursor()
    # writing the query
    query = f'SELECT name,goal,middle,start from {table_name}'
    # execute query & fetch results
    cursor.execute(query)
    get_all = cursor.fetchall()
    connect_sql.close()

    return get_all

