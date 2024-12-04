#!/bin/bash

# Paths
LOG_PATH="/logs/sanitized.log"
REPORT_PATH="/app/report.html"

# Generate the report
if [ -f "$LOG_PATH" ]; then
    echo "Generating report..."
    goaccess $LOG_PATH --config-file=/app/goaccess.conf -o $REPORT_PATH
else
    echo "Log file not found at $LOG_PATH. Creating a placeholder report..."
    echo "<h1>No logs found</h1>" > $REPORT_PATH
fi

# Serve the report via HTTP server
echo "Starting HTTP server to serve the report..."
cd /app
python3 -m http.server 8080
