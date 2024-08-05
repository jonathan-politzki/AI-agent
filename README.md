# AI-Powered Data Generator

This project uses AI to analyze a given dataset and generate similar data. It's designed to work with CSV files containing exercise information but can be adapted for other structured data types.

## Features

- Analyzes input CSV files using Anthropic's Claude AI
- Generates new data rows based on the analysis
- Handles errors with retry logic
- Runs in a Docker container for easy deployment and consistency

## Prerequisites

- Docker
- Anthropic API key

## Setup

1. Clone this repository
2. Place your input CSV file in the `data` directory
3. Build the Docker image:


## Usage

1. Run the Docker container:

2. When prompted, enter your Anthropic API key
3. Provide the name of your input CSV file (e.g., `input.csv`)
4. Specify the number of new data rows you want to generate

The generated data will be saved in `/app/data/new_dataset.csv` within the container, which is mapped to the `data` directory on your host machine.

## File Structure

- `agents.py`: Main script containing the analysis and generation logic
- `prompts.py`: Contains prompts for the AI agents
- `Dockerfile`: Defines the Docker image for the project
- `requirements.txt`: Lists Python dependencies
- `data/`: Directory for input and output CSV files

## Customization

To adapt this for different data types, modify the `ANALYZER_SYSTEM_PROMPT` and `GENERATOR_SYSTEM_PROMPT` in `prompts.py` to suit your specific data structure and requirements.

## License

[Specify your license here]

## Contributing

[Instructions for contributing to your project]