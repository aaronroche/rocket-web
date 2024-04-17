#!/bin/bash

# Define the table name
TABLE_NAME="rocket-web"

# Delete the DynamoDB table
aws dynamodb delete-table --region us-east-1 --table-name $TABLE_NAME

# Check if the table was deleted successfully
if [ $? -eq 0 ]; then
    echo "Table $TABLE_NAME deleted successfully."
else
    echo "Failed to delete table $TABLE_NAME."
fi
