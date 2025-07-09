#!/bin/bash

# Ask the user to input their preferred log level
echo "Enter the log level (DEBUG, INFO, WARNING, ERROR, CRITICAL):"
read LOG_LEVEL

# Create the .env file if it does not exist
if [ ! -e .env ]; then
    touch .env
fi

# Write the log level to the .env file
if [ -z "$LOG_LEVEL" ]; then
    echo "No log level provided. Defaulting to INFO."
    LOG_LEVEL="INFO"  # Default to INFO if no input is provided
fi

# Write or update the LOG_LEVEL in the .env file
if grep -q "^LOG_LEVEL=" ./.env; then
    sed -i "s#^LOG_LEVEL=.*#LOG_LEVEL=$LOG_LEVEL#" ./.env
else
    echo "LOG_LEVEL=$LOG_LEVEL" >> ./.env
fi