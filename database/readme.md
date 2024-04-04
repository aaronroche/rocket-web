# Database Scripts

## Build Script 
- the build script is a bash script to run it
- `chmod +x create_dynamodb_table.sh`
- Then run it using: `./create_dynamodb_table.sh`

## Python CRUD Script for database
- models.py contain the schema for the crud operations to follow
CRUD.py 
- Contains a `write` function to add elements to database 
- Contains a `read` function to pull data(for testing in this case)
- A `delete all` to remove all the tables data
- Also added drivers for testing

### Dependencies
To run this you will need the following Python libraries installed
- pydantic for schema 
- boto3 for interactions with db

### Note:
Ensure all paths are relative and lead to correct folders for the python files