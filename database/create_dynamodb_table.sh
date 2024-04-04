#!/bin/bash

# Define the table parameters
TABLE_NAME="rocket-web"
PARTITION_KEY_NAME="uid"
PARTITION_KEY_TYPE="N"
READ_CAPACITY_UNITS=5
WRITE_CAPACITY_UNITS=5

# Create the DynamoDB table
aws dynamodb create-table --region us-east-1 \
  --table-name $TABLE_NAME \
  --attribute-definitions AttributeName=$PARTITION_KEY_NAME,AttributeType=$PARTITION_KEY_TYPE \
  --key-schema AttributeName=$PARTITION_KEY_NAME,KeyType=HASH \
  --provisioned-throughput ReadCapacityUnits=$READ_CAPACITY_UNITS,WriteCapacityUnits=$WRITE_CAPACITY_UNITS

# Check if the table was created successfully
if [ $? -eq 0 ]; then
    echo "Table $TABLE_NAME created successfully."
else
    echo "Failed to create table $TABLE_NAME."
fi
