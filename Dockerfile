FROM ubuntu:latest

# Install required packages
RUN apt-get update && apt-get install -y \
    goaccess \
    curl \
    python3 && \
    apt-get clean

# Set up the working directory
WORKDIR /app

# Copy configuration and scripts
COPY goaccess.conf /app/goaccess.conf
COPY run.sh /app/run.sh

# Make the script executable
RUN chmod +x /app/run.sh

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
