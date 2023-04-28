import json
import sys

def set_environment_variables(json_data):
    for key, value in json_data.items():
        if isinstance(value, list):
            # Convert lists to JSON string format
            value = json.dumps(value)
        # Use underscore (_) in place of spaces in the key
        key = key.replace(' ', '_').upper()
        # Output the environment variable assignment
        sys.stdout.write(f"{key}={value}\n")

if __name__ == "__main__":
    json_data = json.loads(sys.stdin.read())
    set_environment_variables(json_data)