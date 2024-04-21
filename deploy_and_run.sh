#!/bin/bash

# Deploy all stacks
cdk deploy --all --require-approval never

# Check if CDK deploy was successful
if [ $? -eq 0 ]; then
    echo "CDK deploy successful, running the event_bridge.sh script..."
    ./event_bridge.sh
else
    echo "CDK deploy failed, not running the event_bridge.sh script."
fi