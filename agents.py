# agents.py

# importing necessary libraries
import os
import csv
import numpy
import anthropic
from prompts import *

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


def analyzer_agent(sample_data):
    message = client.messages.create(
        model=sonnet,
        max_tokens=200, # limit the response to 200 tokens
        temperature=0.1, # a lower temperature leads to a more focused, deterministic output (what does this really mean?)
        system=ANALYZER_SYSTEM_PROMPT, # use the predefined system prompt for the analyzer
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
                # format the user prompt with the sample data
            }
        ]
    )
    return message.content[0].text # return the content of the first message in the response

def generator_agent(analysis_results, sample_data, num_rows=30):
    message = client.messages.create(
        model=sonnet,
        max_tokens=1500, # limit the response to 200 tokens
        temperature=1, # a lower temperature leads to a more focused, deterministic output
        system=GENERATOR_SYSTEM_PROMPT, # use the predefined system prompt for the generator
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_results=analysis_results,
                    sample_data=sample_data
                    )
                # format the user prompt with the analysis results, sample data, and number of rows
            }
        ]
    )

# main execution flow

# get input file path from the user
file_path = input("\Enter the path to the CSV file: ")
file_path = os.path.join('/app/data', file_path) # join the file path with the data directory
desired_rows = int(input("Enter the number of rows you want to generate: ")) # get the desired number of rows from the user

# read the sample data from the input to the CSV file
sample_data = read_csv(file_path)
sample_data_str = "\n".join([",".join(row) for row in sample_data]) # converts 2d to string

# print statements to update user
print("\nLaunching team of agents...")

analysis_result = analyzer_agent(sample_data_str) # analyze the sample data
print("\nAnalyzer agent output: ####\n")

print(analysis_result)
print("\n-----------------------------------\n\nGenerating new data...")

# set up the output file
output_file = "/app/data/new_dataset.csv"
headers = sample_data[0] # get the headers from the sample data
 
# create the output file with headers
save_to_csv("", output_file, headers=headers)

# generated data in batches until we reach the desired number of rows
while generated_rows < desired rows:
    # calculate the number of rows to generate in this batch
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    # generate a batch of data using the Generator Agent
    generated_data = generator_agent(analysis_result, sample_data_str, rows_to_generate)
    # append the generated data to the output file
    save_to_csv(generated_data, output_file)
    # update the count of generated rows
    generated_rows += rows_to_generate
    # print progress update
    print(f"Generated {generated_rows} rows out of {desired_rows}")

# inform the user that the process is complete
print(f"\nGenerated data has been saved to {output_file}")
