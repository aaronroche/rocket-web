from pydantic import BaseModel
from typing import List

class DynamoDBItemSchema(BaseModel):
    uid: int
    title: str
    payload: str
    company: str
    details: List[str]
