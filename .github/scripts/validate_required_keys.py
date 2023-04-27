import json
import argparse

import yaml

# Define prohibited values
prohibited_values = ["None", "", "None", "[]"]

# Function to validate required keys
def validate_required_keys(json_data, required_keys):
    missing_keys = [key for key in required_keys if key not in json_data]
    if missing_keys:
        raise ValueError(f"Missing required keys: {', '.join(missing_keys)}")
    return True

# Function to validate values (ensure they don't match prohibited values)
def validate_values(json_data, required_keys):
    for i, key in enumerate(required_keys):
        value = json_data.get(key)
        prohibited_value = prohibited_values[i]
        if str(value) == prohibited_value:
            raise ValueError(f"Prohibited value detected for key '{key}': '{value}'")
    return True

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

    # Validate required keys
    validate_required_keys(json_data, required_keys)

    # Validate values
    validate_values(json_data, required_keys)

    print("All validations passed.")

# Use argparse to handle command-line arguments
parser = argparse.ArgumentParser(description="Validate JSON file and keys.")
parser.add_argument("json_file", help="Path to the JSON file.")
parser.add_argument("required_keys_file", help="Path to the YAML file containing required keys.")
args = parser.parse_args()

# Example usage (CLI arguments: JSON file path and required keys YAML file path)
main(args.json_file, args.required_keys_file)
