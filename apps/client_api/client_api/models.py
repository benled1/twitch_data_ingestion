from typing import Annotated, Dict, Optional, List, Any
from pydantic import BaseModel, Field
from pydantic_core import core_schema
from bson import ObjectId
from bson.errors import InvalidId
from datetime import datetime

class PyObjectId(ObjectId):
    """
    Custom type to allow use of MongoDB ObjectId type in Pydantic
    """
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> core_schema.CoreSchema:
        return core_schema.no_info_plain_validator_function(cls._validate)
    
    @classmethod
    def _validate(cls, value: Any) -> str:
        if isinstance(value, ObjectId):
            return str(value)
        if isinstance(value, str):
            try:
                return str(ObjectId(value))
            except InvalidId:
                raise ValueError("Invalid ObjectId string")
        raise TypeError("ObjectId must be a string or ObjectId instance")

class Channel(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id")]
    channel: str
    metadata: Optional[Dict[str, List[Dict[Any, Any]]]]

class ChannelCoordinates(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id")]
    channel: str
    coords: List[float]
    month: datetime
    ts: datetime

class NodePosition(BaseModel):
    x: float
    y: float
    z: float

class ChannelNode(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id")]
    channel: str
    month: datetime
    position: NodePosition
    ts: datetime

class ChannelEdge(BaseModel):
    id: Annotated[PyObjectId, Field(alias="_id")]
    month: datetime
    source_id: str
    target_id: str
    ts: datetime
    value: float
    