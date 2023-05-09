import argparse
import json

def check_elements(json_string):
    # Load the JSON string into a Python list
    data = json.loads(json_string)
    # Convert list to a set
    data_set = set(data)

    # this is how we set the issue type dynamically based on the labels
    # we can add more labels to the sets below to add more issue types
    if {'org', 'webhook'}.issubset(data_set):
        print("org-webhook")
    elif {'repo', 'webhook'}.issubset(data_set):
        print("repo-webhook")
    else:
        return "invalid issue type"

def main():
    parser = argparse.ArgumentParser(description='Check for specific elements in a JSON string.')
    parser.add_argument('-j', '--json', required=True, help='The JSON string to check.')

    args = parser.parse_args()

    result = check_elements(args.json)
    print(result)

if __name__ == "__main__":
    main()
