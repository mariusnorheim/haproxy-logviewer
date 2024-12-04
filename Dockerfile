FROM ubuntu:latest

# Install required packages
RUN apt-get update && apt-get install -y \
    goaccess \
    curl \
    python3 \
    locales && \
    apt-get clean
RUN locale-gen en_US.UTF-8 && \
    update-locale LANG=en_US.UTF-8 \
    update-locale LC_ALL=en_US.UTF-8

ENV LANG en_US.UTF-8
ENV LC_ALL en_US.UTF-8

# Set up the working directory
WORKDIR /app

# Copy configuration and scripts
COPY goaccess.conf /app/goaccess.conf
COPY run.sh /app/run.sh

# Make the script executable
RUN chmod +x /app/run.sh

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
