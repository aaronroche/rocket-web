import boto3
from pydantic import ValidationError
from models import DynamoDBItemSchema

def create_dynamodb_client(region_name='us-east-1'):
    return boto3.client('dynamodb', region_name=region_name)

def write_to_dynamodb(table_name, item_data):
    client = create_dynamodb_client()
    try:
        # Validate item_data using the schema
        validated_data = DynamoDBItemSchema(**item_data)

        # Convert Pydantic model to a dictionary suitable for DynamoDB
        item = {
            'uid': {'N': str(validated_data.uid)},
            'title': {'S': validated_data.title},
            'payload': {'S': validated_data.payload},
            'company': {'S': validated_data.company},
            'details': {'L': [{'S': detail} for detail in validated_data.details]}
        }

        # Write to DynamoDB
        response = client.put_item(TableName=table_name, Item=item)
        return response
    except ValidationError as e:
        # Handle the validation error
        print("Validation error:", e.json())
        return None

def read_from_dynamodb(table_name, uid):
    client = create_dynamodb_client()
    response = client.get_item(
        TableName=table_name,
        Key={
            'uid': {'N': str(uid)}
        }
    )
    return response.get('Item', {})

def delete_all_items(table_name):
    client = create_dynamodb_client()
    # Scanning the table to get all items
    response = client.scan(TableName=table_name)
    items = response.get('Items', [])

    # Iterate over the items and delete each one
    for item in items:
        key = {k: v for k, v in item.items() if k in ["uid"]} 
        client.delete_item(TableName=table_name, Key=key)

    print(f"Deleted {len(items)} items from {table_name}")

# Example usage

# item_data = {
#     "uid": 101,
#     "title": "Mission 1",
#     "payload": "Satellite",
#     "company": "SpaceX",
#     "details": ["First stage landing on drone ship", "Deploying in low Earth orbit"]
# }
# response = write_to_dynamodb(table_name, item_data)
# if response:
#     print("Write response:", response)
# schema
# {
#         title: String,
#         payload: String,
#         company: String,
#         details: [String]  
# }

# print("Write response:", response)
# read_response = read_from_dynamodb(table_name, 101)
# print("Read response:", read_response)

# table_name = "rocket-web"
# delete_all_items(table_name)