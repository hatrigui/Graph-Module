from pydantic import BaseModel, field_validator
from typing import List, Optional

class Node(BaseModel):
    title: str
    description: Optional[str] = None
    condition: Optional[str] = None
    links: List[str] = []

    @field_validator('condition', mode='before')
    def validate_condition(cls, v):
        if v is not None:
            import re
            pattern = r'^(?:\$[\w]+(?:\s+(?:AND|OR)\s+\$[\w]+)*)$'
            if not re.match(pattern, v):
                raise ValueError('Condition must be a logical expression using $variables, AND, OR')
        return v

class NodeResponse(Node):
    id: str


