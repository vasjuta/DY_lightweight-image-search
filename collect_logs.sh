#!/bin/bash

# Create logs directory if it doesn't exist
mkdir -p logs

# Get timestamp for log file name
timestamp=$(date +%Y%m%d_%H%M%S)
logfile="logs/system_log_${timestamp}.log"

echo "System Log - $(date)" > $logfile
echo "-------------------" >> $logfile

# Collect logs from all services
for service in downloader embedding_service qdrant indexer web_ui; do
    echo "Logs from $service:" >> $logfile
    echo "-------------------" >> $logfile
    docker compose logs $service >> $logfile 2>&1
    echo "\n" >> $logfile
done

echo "Log file created at: $logfile"