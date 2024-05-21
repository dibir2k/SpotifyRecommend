#!/bin/bash

# Run the script to create the collection
python create_collection.py

# Check if the script ran successfully
if [ $? -ne 0 ]; then
  echo "Failed to run create_collection.py"
  exit 1
fi

# Start the Flask application
python wsgi.py
