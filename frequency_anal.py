import sqlite3
import pandas as pd
import os

# Specify the full path to the SQLite database
db_path = 'database/boards.db'

# Debugging: Print the database path
print(f"Database path: {db_path}")

# Set pandas display options to show more rows and columns
pd.set_option('display.max_rows', 100)  # Adjust this value as needed
pd.set_option('display.max_columns', None)  # Show all columns

# Check if the file exists
if not os.path.exists(db_path):
    print("Database file does not exist.")
else:
    print("Database file found. Attempting to connect...")

    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        
        # Retrieve the data from the V3 table
        v3_data_query = "SELECT * FROM V3;"
        v3_data = pd.read_sql(v3_data_query, conn)

        # Debugging: Print the first few rows of the retrieved data
        print("Retrieved V3 Data:")
        print(v3_data.head())

        # Combine 'goal', 'start', and 'middle' columns into a single series
        middle_split = v3_data['middle'].str.split(',', expand=True).stack().reset_index(level=1, drop=True)

        # Debugging: Print the middle split data
        print("Middle Split Data:")
        print(middle_split.head(20))

        # Concatenate the Series
        combined_data = pd.concat([v3_data['goal'], v3_data['start'], middle_split])

        # Debugging: Print the combined data
        print("Combined Data:")
        print(combined_data.head(20))

        # Calculate the frequency of each unique value in the combined series
        combined_frequency = combined_data.value_counts().reset_index()
        combined_frequency.columns = ['value', 'frequency']

        # Debugging: Print the combined frequency data
        print("Combined Frequency Data:")
        print(combined_frequency.head(100))

        # Display the frequency dataframe
        print("Combined Frequency in V3:")
        print(combined_frequency)
    except sqlite3.OperationalError as e:
        print(f"SQLite error: {e}")
    finally:
        conn.close()
