from pydantic import BaseModel
from typing_extensions import TypedDict

def basemodel_to_typeddict(model: BaseModel):
    return TypedDict('NewTypedDict', **{k: v.outer_type_ for k, v in model.items()})