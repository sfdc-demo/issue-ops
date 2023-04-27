import argparse
import json
import sys

import yaml


def read_yaml_file(file_path):
    with open(file_path, "r") as file:
        file_content = file.read()
    return yaml.safe_load(file_content)


def find_owner(instance_list, github_instance, organization_name, username):
    instance = next(
        (
            inst
            for inst in instance_list["github_instances"]
            if inst["instance"] == github_instance
        ),
        None,
    )
    if not instance:
        sys.exit(1)

    organization = next(
        (
            org
            for org in instance["organizations"]
            if org["name"] == organization_name),
        None,
    )
    if not organization:
        sys.exit(1)

    if username in organization["owners"]:
        return json.dumps({
            "instance": instance["instance"],
            "url": instance["url"],
            "name": organization["name"],
            "owner": username,
        })
    else:
        sys.exit(1)


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
result = find_owner(instance_list, args.github_instance, args.organization, args.user)

print(result)
