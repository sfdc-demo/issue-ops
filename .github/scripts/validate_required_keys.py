import argparse
import json
import os

import yaml


# Define prohibited values
prohibited_values = ["None", "", "None", "[]"]

# Function to validate required keys
def validate_required_keys(json_data, required_keys, errors):
    missing_keys = [key for key in required_keys if key not in json_data]
    if missing_keys:
        errors['missing_keys'] = missing_keys

# Function to validate values (ensure they don't match prohibited values)
def validate_values(json_data, required_keys, errors):
    prohibited_value_errors = []
    for key in required_keys:
        value = json_data.get(key)
        if str(value) in prohibited_values:
            prohibited_value_errors.append({key: value})
    if prohibited_value_errors:
        errors['prohibited_values'] = prohibited_value_errors

# Function to read required keys from YAML file
def read_required_keys(required_keys_file):
    with open(required_keys_file) as f:
        data = yaml.safe_load(f)
        required_keys = data.get('required_keys', [])
    return required_keys

# Main function to read JSON data from file and validate keys and values
def main(json_file, required_keys_file):
    with open(json_file) as f:
        json_data = json.load(f)

    # Read required keys from YAML file
    required_keys = read_required_keys(required_keys_file)

    # Initialize an empty dictionary to store errors
    errors = {}

    # Validate required keys
    validate_required_keys(json_data, required_keys, errors)

    # Validate values
    validate_values(json_data, required_keys, errors)

    # Check if there are any errors
    if errors:
        print(json.dumps(errors))
    else:
        print("")

parser = argparse.ArgumentParser(
    description="Validate JSON file and keys."
)
parser.add_argument(
    "-j",
    "--json_file",
    dest="json_file",
    type=str,
    required=True,
    help="Path to the JSON file."
)
parser.add_argument(
    "-k",
    "--required_keys_file",
    dest="required_keys_file",
    type=str,
    required=True,
    help="Path to the YAML file containing required keys."
)

args = parser.parse_args()

# Example usage (CLI arguments: JSON file path and required keys YAML file path)
main(args.json_file, args.required_keys_file)
