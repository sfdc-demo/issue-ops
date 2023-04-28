import argparse
import json

import yaml


# Define a list of prohibited values.
prohibited_values = ["None", "", "None", "[]"]

# Define a function to validate the presence of required keys in the JSON data.
def validate_required_keys(json_data, required_keys, errors):
    missing_keys = [key for key in required_keys if key not in json_data]
    if missing_keys:
        errors["missing_keys"] = missing_keys

# Define a function to validate that the values of required keys do not match prohibited values.
def validate_values(json_data, required_keys, errors):
    prohibited_value_errors = []
    for key in required_keys:
        value = json_data.get(key)
        if str(value) in prohibited_values:
            prohibited_value_errors.append({key: value})
    if prohibited_value_errors:
        errors["prohibited_values"] = prohibited_value_errors

# Define a function to read and parse required keys from a YAML file.
def read_required_keys(required_keys_file):
    with open(required_keys_file) as f:
        data = yaml.safe_load(f)
        required_keys = data.get("required_keys", [])
    return required_keys

# Define the main function to read JSON data from a file, validate keys and values, and print errors (if any).
def main(json_file, required_keys_file):
    # Read and parse the JSON data from the provided file.
    with open(json_file) as f:
        json_data = json.load(f)

    # Read the list of required keys from the YAML file.
    required_keys = read_required_keys(required_keys_file)

    # Initialize an empty dictionary to store errors.
    errors = {}

    # Validate the presence of required keys in the JSON data.
    validate_required_keys(json_data, required_keys, errors)

    # Validate that the values of required keys do not match prohibited values.
    validate_values(json_data, required_keys, errors)

    # Check if there are any errors and print them as JSON.
    if errors:
        print(json.dumps(errors))
    else:
        print("")

# Set up an argument parser to handle command-line arguments.
parser = argparse.ArgumentParser(description="Validate JSON file and keys.")
parser.add_argument("-j", "--json_file", required=True, help="Path to the JSON file.")
parser.add_argument("-k", "--required_keys_file", required=True, help="Path to the YAML file containing required keys.")

# Parse command-line arguments and call the main function.
args = parser.parse_args()
main(args.json_file, args.required_keys_file)