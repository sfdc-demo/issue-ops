import argparse
import json

import yaml


def create_payload(github_yaml_file, user, issue_json_file, issue_number, issue_title):
    # Read and parse the YAML from the github_yaml_file
    with open(github_yaml_file, "r") as yaml_file:
        github_data = yaml.safe_load(yaml_file)

    # Create a mapping between GitHub instances and their corresponding URLs
    instance_to_url = {
        item["instance"]: item["url"]
        for item in github_data.get("github_instances", [])
    }

    # Read and parse the JSON from the issue_json_file
    with open(issue_json_file, "r") as json_file:
        issue_json = json.load(json_file)

    # Replace 'instance' key value with the corresponding URL
    instance_key = issue_json.get("instance")
    if instance_key in instance_to_url:
        issue_json["instance"] = instance_to_url[instance_key]

    # Create a dictionary to store the provided arguments and modified JSON data
    payload = {
        "github_data": github_data,
        "user": user,
        "issue_json": issue_json,
        "issue_number": issue_number,
        "issue_title": issue_title,
    }
    # Return the payload dictionary
    return payload


def main():
    # Set up command-line argument parser
    # Set up command-line argument parser
    parser = argparse.ArgumentParser(description='Create payload from command-line arguments.')
    parser.add_argument('-g', '--github_yaml', required=True, help='Path to GitHub YAML file')
    parser.add_argument('-u', '--user', required=True, help='User name')
    parser.add_argument('-j', '--issue_json', required=True, help='Path to issue JSON file')
    parser.add_argument('-n', '--issue_number', required=True, help='Issue number')
    parser.add_argument('-t', '--issue_title', required=True, help='Issue title')
    # Parse command-line arguments
    args = parser.parse_args()

    # Call the create_payload function with parsed arguments
    payload = create_payload(
        args.github_yaml,
        args.user,
        args.issue_json,
        args.issue_number,
        args.issue_title,
    )

    # Print the payload dictionary as JSON
    print(json.dumps(payload))


if __name__ == "__main__":
    main()
