import argparse
import json
import sys

import yaml


def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
    return yaml.safe_load(file_content)


def find_owner(instance_list, github_instance, organization_name, username):
    error_messages = {}
    instance = next(
        (
            inst
            for inst in instance_list["github_instances"]
            if inst["instance"] == github_instance
        ),
        None,
    )
    if not instance:
        error_messages["instance_error"] = "Instance not found."
        return None, error_messages

    organization = next(
        (
            org
            for org in instance["organizations"] # type: ignore
            if org["name"] == organization_name),
        None,
    )
    if not organization:
        error_messages["organization_error"] = "Organization not found."
        return None, error_messages

    # User validation
    if username in organization["owners"] and not error_messages:
        return None
    else:
        error_messages["owner_error"] = "User is not an owner."
        return error_messages


parser = argparse.ArgumentParser(
    description="validate github roles"
)
parser.add_argument(
    "-g",
    "--github_instance",
    type=str,
    required=True,
    help="Name of the GitHub instance",
)
parser.add_argument(
    "-o",
    "--organization",
    type=str,
    required=True,
    help="Name of the organization"
)
parser.add_argument(
    "-u",
    "--user",
    type=str,
    required=True,
    help="user (github.actor) to validate"
)

args = parser.parse_args()

instance_list = read_yaml_file(".github/PERMISSIONS/github.yml")
result, errors = find_owner(instance_list, args.github_instance, args.organization, args.user) # type: ignore

if errors:
    print(json.dumps(errors))
else:
    print(result)
