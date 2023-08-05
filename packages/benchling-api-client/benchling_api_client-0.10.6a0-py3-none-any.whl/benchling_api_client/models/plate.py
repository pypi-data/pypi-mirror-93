import datetime
from typing import Any, Dict, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.fields import Fields
from ..models.plate_wells import PlateWells
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Plate:
    """  """

    fields: Fields
    id: str
    barcode: Union[Unset, Optional[str]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    creator: Union[UserSummary, Unset] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    parent_storage_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, Optional[str]] = UNSET
    schema: Union[SchemaSummary, Unset] = UNSET
    wells: Union[PlateWells, Unset] = UNSET

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

        name = self.name
        parent_storage_id = self.parent_storage_id
        project_id = self.project_id
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        wells: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.wells, Unset):
            wells = self.wells.to_dict()

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
        if name is not UNSET:
            field_dict["name"] = name
        if parent_storage_id is not UNSET:
            field_dict["parentStorageId"] = parent_storage_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if wells is not UNSET:
            field_dict["wells"] = wells

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Plate":
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

        name = d.pop("name", UNSET)

        parent_storage_id = d.pop("parentStorageId", UNSET)

        project_id = d.pop("projectId", UNSET)

        schema: Union[SchemaSummary, Unset] = UNSET
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], _schema))

        wells: Union[PlateWells, Unset] = UNSET
        _wells = d.pop("wells", UNSET)
        if _wells is not None and not isinstance(_wells, Unset):
            wells = PlateWells.from_dict(cast(Dict[str, Any], _wells))

        plate = Plate(
            fields=fields,
            id=id,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            project_id=project_id,
            schema=schema,
            wells=wells,
        )

        return plate
