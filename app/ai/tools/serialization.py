from __future__ import annotations

from dataclasses import asdict, is_dataclass

from datetime import datetime 
from typing import Any 

def to_jsonable(value: Any) -> Any:
    """Convert service results into values that an LLM tool can understand properly"""
    #convert dataclass objects such as LearnerState into dictionaries 
    if is_dataclass(value) and not isinstance(value, type):
        return to_jsonable(asdict(value))

    #Convert dates into readable text. 
    if isinstance(value, datetime):
        return value.isoformat()
    # Convert every value inside a dictionary.
    if isinstance(value, dict):
        return {
            key: to_jsonable(item)
            for key, item in value.items()
        }
    # Convert every value inside a list or tuple.
    if isinstance(value, (list, tuple)):
        return [to_jsonable(item) for item in value]
    # Strings, numbers, booleans and None are already safe.
    return value
