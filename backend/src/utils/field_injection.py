from typing import Type, TypedDict
from pydantic import BaseModel, create_model

def inject_fields(typed_dict: Type[TypedDict]) -> BaseModel: 
    def decorator(cls):
        fields = {key: (value, ...) for key, value in typed_dict.__annotations__.items()} 
        new_model = create_model(cls.__name__, **fields) 
        return new_model 
    return decorator