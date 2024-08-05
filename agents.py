# agents.py

import os
import csv
import numpy
import anthropic
from prompts import *
import time
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def analyzer_agent_with_retry(sample_data):
    return analyzer_agent(sample_data)

@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=4, max=10))
def generator_agent_with_retry(analysis_results, sample_data, num_rows=30):
    return generator_agent(analysis_results, sample_data, num_rows)


print("Contents of /app/data:")
print(os.listdir('/app/data'))

if not os.getenv("ANTHROPIC_API_KEY"):
    os.environ["ANTHROPIC_API_KEY"] = input("Please enter your Anthropic API key: ")

client = anthropic.Anthropic()

def read_csv(file_path):
    data = []
    with open(file_path, 'r', newline="") as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data

def save_to_csv(data, output_file, headers=None):
    mode = 'w' if headers else 'a'
    with open(output_file, mode, newline="") as f:
        writer = csv.writer(f)
        if headers:
            writer.writerow(headers)
        if isinstance(data, str):
            for row in csv.reader(data.splitlines()):
                writer.writerow(row)
        elif isinstance(data, list):
            for row in data:
                if isinstance(row, str):
                    writer.writerow(row.split(','))
                elif isinstance(row, list):
                    writer.writerow(row)
                else:
                    print(f"Skipping invalid row: {row}")
        else:
            print(f"Unsupported data type: {type(data)}")

def analyzer_agent(sample_data):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=200,
        temperature=0.1,
        system=ANALYZER_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": ANALYZER_USER_PROMPT.format(sample_data=sample_data)
            }
        ]
    )
    return message.content

def generator_agent(analysis_results, sample_data, num_rows=30):
    message = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=1500,
        temperature=1,
        system=GENERATOR_SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": GENERATOR_USER_PROMPT.format(
                    num_rows=num_rows,
                    analysis_results=analysis_results,
                    sample_data=sample_data
                )
            }
        ]
    )
    # Process the generated content
    if isinstance(message.content, list) and len(message.content) > 0:
        content = message.content[0].text
    else:
        content = str(message.content)
    
    # Split the content into individual rows
    rows = content.strip().split('\n')
    return rows

# Main execution flow
while True:
    file_name = input("\nEnter the name of the CSV file (e.g., input.csv): ")
    file_path = os.path.join('/app/data', file_name)
    if os.path.exists(file_path):
        print(f"File found: {file_path}")
        break
    else:
        print(f"File not found: {file_path}")
        print("Please make sure the file is in the 'data' directory and try again.")

try:
    sample_data = read_csv(file_path)
    sample_data_str = "\n".join([",".join(row) for row in sample_data])
    print(f"Successfully read {len(sample_data)} rows from {file_name}")
except Exception as e:
    print(f"Error reading the CSV file: {e}")
    exit(1)

desired_rows = int(input("Enter the number of rows you want to generate: "))

print("\nLaunching team of agents...")

analysis_result = analyzer_agent_with_retry(sample_data_str)
print("\nAnalyzer agent output: ####\n")
print(analysis_result)
print("\n-----------------------------------\n\nGenerating new data...")

output_file = "/app/data/new_dataset.csv"
headers = sample_data[0]

save_to_csv("", output_file, headers=headers)

generated_rows = 0
batch_size = 10

while generated_rows < desired_rows:
    rows_to_generate = min(batch_size, desired_rows - generated_rows)
    generated_data = generator_agent_with_retry(analysis_result, sample_data_str, rows_to_generate)
    save_to_csv(generated_data, output_file)
    generated_rows += len(generated_data)
    print(f"Generated {generated_rows} rows out of {desired_rows}")

print(f"\nGenerated data has been saved to {output_file}")