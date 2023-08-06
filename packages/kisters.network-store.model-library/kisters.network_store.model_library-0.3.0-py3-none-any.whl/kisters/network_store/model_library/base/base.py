import enum
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Union

from pydantic import BaseModel, Extra, Field, constr, validator


class Model(BaseModel):
    class Config:
        extra = Extra.forbid


UserMetadataKey = constr(regex=r"^\w+$")


class BaseElement(Model):
    domain: Optional[str] = None
    element_class: Optional[str] = None
    uid: str = Field(..., regex="^[a-zA-Z]\\w*$", description="Unique identifier")
    display_name: Optional[str] = Field(
        None, description="String for labeling an element in a GUI"
    )
    created: Optional[datetime] = Field(
        None, description="Timestamp element was added to the network"
    )
    deleted: Optional[datetime] = Field(
        None, description="Timestamp element was removed from the network"
    )
    group_uid: Optional[str] = Field(
        None, description="UID of group to which link belongs"
    )
    user_metadata: Optional[Dict[UserMetadataKey, Union[float, str]]] = Field(
        None, description="Optional dictionary of user-provided key-value pairs"
    )

    @validator("display_name", always=True)
    def default_display_name(cls, v: Any, values: Dict[str, Any]) -> Any:
        return v or values.get("uid")


class Location(Model):
    x: float
    y: float
    z: float = 0.0


class LocationSet(str, enum.Enum):
    GEOGRAPHIC = "location"
    SCHEMATIC = "schematic_location"


class LocationExtent(BaseModel):
    """Mapping of dimensions to range, e.g. {"x": [-10, 10]}"""

    x: Optional[Tuple[float, float]] = None
    y: Optional[Tuple[float, float]] = None
    z: Optional[Tuple[float, float]] = None


class BaseLink(BaseElement):
    collection: str = Field("links", const=True)
    source_uid: str = Field(..., description="UID of source node")
    target_uid: str = Field(..., description="UID of target node")
    vertices: Optional[List[Location]] = Field(
        None,
        description="Additional geographical points refining the path"
        " from source to target nodes",
    )
    schematic_vertices: Optional[List[Location]] = Field(
        None,
        description="Additional schematic points refining the path"
        " from source to target nodes",
    )


class BaseNode(BaseElement):
    collection: str = Field("nodes", const=True)
    location: Location = Field(..., description="Geographical location")
    schematic_location: Optional[Location] = Field(
        None, description="Schematic location. Takes value of 'location' if unset."
    )

    @validator("schematic_location", always=True)
    def default_schematic_location(cls, v: Any, values: Dict[str, Any]) -> Any:
        if v is None:
            return values.get("location")
        return v


class BaseGroup(BaseNode):
    collection: str = Field("groups", const=True)
