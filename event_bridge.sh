#!/bin/bash

REGION="us-east-1"
ACCOUNT_ID="620339869704"
LAMBDA_FUNCTION_NAME="rocket-web-lambda"
RULE_NAME="WeeklyRocketWebTrigger"
STATEMENT_ID="eventbridge-access-${RANDOM}"

aws lambda add-permission \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --statement-id ${STATEMENT_ID} \
    --action 'lambda:InvokeFunction' \
    --principal events.amazonaws.com \
    --source-arn "arn:aws:events:${REGION}:${ACCOUNT_ID}:rule/${RULE_NAME}"

aws events put-rule \
    --name ${RULE_NAME} \
    --schedule-expression "rate(7 days)" \
    --state ENABLED

aws events put-targets \
    --rule ${RULE_NAME} \
    --targets "Id"="1","Arn"="arn:aws:lambda:${REGION}:${ACCOUNT_ID}:function:${LAMBDA_FUNCTION_NAME}"

aws lambda invoke \
    --function-name ${LAMBDA_FUNCTION_NAME} \
    --payload '{}' \ 
    response.json

echo "Lambda function ${LAMBDA_FUNCTION_NAME} has been triggered immediately and scheduled to run weekly."
