from pydantic import BaseModel
from typing import List

class DeleteScansSchema(BaseModel):
    ids: List[int]
