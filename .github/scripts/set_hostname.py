import argparse
import json

import yaml


# Function to read JSON file
def read_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

# Function to read YAML file
def read_yaml_file(file_path):
    with open(file_path, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
    return data

# Function to find the URL based on the instance value
def find_url(json_data, yaml_data):
    instance_to_find = json_data['instance']
    for instance in yaml_data['github_instances']:
        if instance['instance'] == instance_to_find:
            return instance['url']
    return None

# Define and parse command-line arguments
parser = argparse.ArgumentParser(description='Find URL based on instance value from JSON and YAML files.')
parser.add_argument('--json', required=True, help='Path to the JSON file.')
parser.add_argument('--yaml', required=True, help='Path to the YAML file.')
args = parser.parse_args()

# Read JSON file
json_data = read_json_file(args.json)

# Read YAML file
yaml_data = read_yaml_file(args.yaml)

# Find and print the URL
print(find_url(json_data, yaml_data))
