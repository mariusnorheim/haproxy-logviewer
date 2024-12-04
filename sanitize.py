import re

# Input and output file paths
input_file = "./logs/haproxy.log"
output_file = "./logs/sanitized.log"

def normalize_spaces(file_path):
    """Normalize multi-spaces to single spaces in the log file."""
    with open(file_path, "r") as infile:
        lines = infile.readlines()

    # Normalize spaces in each line
    normalized_lines = [re.sub(r'\s+', ' ', line.strip()) for line in lines]

    # Overwrite the original file with normalized lines
    with open(file_path, "w") as outfile:
        outfile.write("\n".join(normalized_lines) + "\n")

# Normalize spaces in the input log file
normalize_spaces(input_file)

def extract_fields(line):
    """Extract required fields from a HAProxy log line."""
    parts = line.split()
    if len(parts) < 20:
        return None

    # Extract the IP address without the port
    ip = parts[5].split(':')[0]

    # Extract the timestamp
    timestamp = parts[6].strip('[]')

    # Extract the HTTP status code
    status_code = parts[17]

    # Extract the session time (Tt field)
    session_time = parts[9].split('/')[-1]

    # Extract the request type (GET/POST)
    request = ' '.join(parts[18:20]).strip('"')

    # Extract the user agent
    user_agent = ' '.join(parts[20:]).strip('"()')

    return ip, timestamp, status_code, session_time, request, user_agent

# Open input and output files
with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        fields = extract_fields(line)
        if fields:
            ip, timestamp, status_code, session_time, request, user_agent = fields
            # Write sanitized log line
            outfile.write(f"{ip} [{timestamp}] {status_code} {session_time} \"{request}\" \"{user_agent}\"\n")
        else:
            # Print unmatched lines for debugging
            print(f"Unmatched line: {line}")