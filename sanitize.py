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

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    for line in infile:
        try:
            # Normalize spaces
            line = ' '.join(line.strip().split())

            # Debug: Print raw log line
            print(f"Processing line: {line}")

            # Split the line into parts
            parts = line.split()

            # Extract IP
            ip = parts[5]  # Field where client IP is located
            if ":" in ip:
                ip = ip.split(':')[0]  # Remove port if present

            # Debug: Print extracted IP
            print(f"Extracted IP: {ip}")

            # Extract timestamp
            raw_timestamp = parts[6].strip('[]')  # Raw timestamp in the format: 4/Dec/2024:07:31:20.408
            timestamp = raw_timestamp.replace(":", " ", 1)  # Replace the first colon (between date and time) with a space

            # Debug: Print extracted timestamp
            print(f"Extracted Timestamp: {timestamp}")

            # Extract session time using regex and keep the `+` prefix
            session_time_match = re.search(r'(\+\d+)', line)
            session_time = session_time_match.group(1) if session_time_match else "UNKNOWN"

            # Debug: Print extracted session time
            print(f"Extracted Session Time: {session_time}")

            # Extract status code using regex
            status_code_match = re.search(r'\s(\d{3})\s', line)
            status_code = status_code_match.group(1) if status_code_match else "UNKNOWN"

            # Debug: Print extracted status code
            print(f"Extracted Status Code: {status_code}")

            # Extract the full HTTP request (entire field within double quotes)
            request_match = re.search(r'"([^"]+)"', line)
            request = request_match.group(1) if request_match else "UNKNOWN"

            # Debug: Print extracted request
            print(f"Extracted Request: {request}")

            # Extract User-Agent
            user_agent_match = re.search(r'\((.*?)\)', line)
            user_agent = user_agent_match.group(1) if user_agent_match else "UNKNOWN"

            # Debug: Print extracted User-Agent
            print(f"Extracted User-Agent: {user_agent}")

            # Write sanitized log line
            sanitized_line = f"{ip} [{timestamp}] {status_code} {session_time} \"{request}\" \"{user_agent}\"\n"
            outfile.write(sanitized_line)

        except Exception as e:
            # Print failed lines with error details
            print(f"Failed to process line: {line} - Error: {e}")
