import datetime
from typing import Any, Dict, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Box:
    """  """

    fields: Fields
    id: str
    barcode: Union[Unset, Optional[str]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[UserSummary, Unset] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    size: Union[Unset, int] = UNSET
    filled_positions: Union[Unset, int] = UNSET
    empty_positions: Union[Unset, int] = UNSET
    empty_containers: Union[Unset, int] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, Optional[str]] = UNSET
    schema: Union[SchemaSummary, Unset] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        fields = self.fields.to_dict()

        id = self.id
        barcode = self.barcode
        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        size = self.size
        filled_positions = self.filled_positions
        empty_positions = self.empty_positions
        empty_containers = self.empty_containers
        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "fields": fields,
                "id": id,
            }
        )
        if barcode is not UNSET:
            field_dict["barcode"] = barcode
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if size is not UNSET:
            field_dict["size"] = size
        if filled_positions is not UNSET:
            field_dict["filledPositions"] = filled_positions
        if empty_positions is not UNSET:
            field_dict["emptyPositions"] = empty_positions
        if empty_containers is not UNSET:
            field_dict["emptyContainers"] = empty_containers
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Box":
        d = src_dict.copy()
        fields = Fields.from_dict(d.pop("fields"))

        id = d.pop("id")

        barcode = d.pop("barcode", UNSET)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        creator: Union[UserSummary, Unset] = UNSET
        _creator = d.pop("creator", UNSET)
        if _creator is not None and not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(cast(Dict[str, Any], _creator))

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        size = d.pop("size", UNSET)

        filled_positions = d.pop("filledPositions", UNSET)

        empty_positions = d.pop("emptyPositions", UNSET)

        empty_containers = d.pop("emptyContainers", UNSET)

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        project_id = d.pop("projectId", UNSET)

        schema: Union[SchemaSummary, Unset] = UNSET
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], _schema))

        web_url = d.pop("webURL", UNSET)

        box = Box(
            fields=fields,
            id=id,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            modified_at=modified_at,
            size=size,
            filled_positions=filled_positions,
            empty_positions=empty_positions,
            empty_containers=empty_containers,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
            web_url=web_url,
        )

        return box
