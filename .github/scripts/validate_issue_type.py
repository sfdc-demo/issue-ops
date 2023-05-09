import argparse
import json

def check_elements(input_string):
    # Load the JSON string into a Python list
    data = input_string.split(',')
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
    parser = argparse.ArgumentParser(description='Check for specific elements in a comma-separated string.')
    parser.add_argument('-s', '--string', required=True, help='The comma-separated string to check.')

    args = parser.parse_args()

    result = check_elements(args.string)
    print(result)

if __name__ == "__main__":
    main()
