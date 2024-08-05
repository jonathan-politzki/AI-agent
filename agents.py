# agents.py

# importing necessary libraries
import os
import csv
import numpy
import anthropic

# set up anthropic key
if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropics API key: ") # prompt the user to enter their API key

# create the anthropic client
client = anthropic.AnthropicClient()
sonnet - "claude-3-5-sonnet-20240620"

# function to read the CSV file from the User
def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline="") as csvfile: # open the CSV file in read mode
        csv_reader = csv.reader(csvfile) # create a CSV reader object
        for row in csv_reader:
            data.append(row)
    return data

# function to save the generated data to a new CSV file
def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a' # Set the file mode: 'w' if headers are provided and 'a' otherwise
    with open(output_file, mode, newline="") as f: # open the CSV file in write mode
        writer = csv.writer(f) # create a CSV writer object
        if headers:
            writer.writerow(headers) # write the headers if provided
        for row in csv.reader(data.splitlines()): # split the data string into rows
            writer.writerow(row) # write the data