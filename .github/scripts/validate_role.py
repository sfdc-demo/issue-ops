import argparse
import json

import yaml


# Define a function to read and parse a YAML file.
def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
    return yaml.safe_load(file_content)


# Define a function to find the owner of a specified GitHub instance and organization.
def find_owner(instance_list, github_instance, organization_name, username):
    error_messages = {}
    # Search for the specified GitHub instance in the instance list.
    instance = next(
        (
            inst
            for inst in instance_list["github_instances"]
            if inst["instance"] == github_instance
        ),
        None,
    )
    # Check if the instance was found.
    if not instance:
        error_messages["instance_error"] = "Instance not found."
        return None, error_messages

    # Search for the specified organization within the found instance.
    organization = next(
        (
            org
            for org in instance["organizations"]
            if org["name"] == organization_name
        ),
        None,
    )
    # Check if the organization was found.
    if not organization:
        error_messages["organization_error"] = "Organization not found."
        return None, error_messages

    # Validate if the user is an owner of the organization.
    if username in organization["owners"] and not error_messages:
        return None, {}  # Return empty dictionary when no errors
    else:
        error_messages["owner_error"] = "User is not an owner."
        return None, error_messages  # Return None as the result when errors are present


# Set up an argument parser to handle command-line arguments.
parser = argparse.ArgumentParser(description="validate github roles")
parser.add_argument("-g", "--github_instance", required=True, help="Name of the GitHub instance")
parser.add_argument("-o", "--organization", required=True, help="Name of the organization")
parser.add_argument("-u", "--user", required=True, help="user (github.actor) to validate")

# Parse command-line arguments.
args = parser.parse_args()

# Read and parse the YAML file containing GitHub instances, organizations, and owners.
instance_list = read_yaml_file(".github/PERMISSIONS/github.yml")
# Call the find_owner function to check for the owner.
result, errors = find_owner(instance_list, args.github_instance, args.organization, args.user)

# Print any errors found during the process, otherwise print "None".
if errors:
    print(json.dumps(errors))
