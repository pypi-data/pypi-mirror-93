from typing import Any, Dict

import attr

from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary


@attr.s(auto_attribs=True)
class Location:
    """  """

    id: str
    barcode: str
    created_at: str
    creator: UserSummary
    fields: Fields
    modified_at: str
    name: str
    parent_storage_id: str
    schema: SchemaSummary
    web_url: str

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        barcode = self.barcode
        created_at = self.created_at
        creator = self.creator.to_dict()

        fields = self.fields.to_dict()

        modified_at = self.modified_at
        name = self.name
        parent_storage_id = self.parent_storage_id
        schema = self.schema.to_dict()

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "barcode": barcode,
                "createdAt": created_at,
                "creator": creator,
                "fields": fields,
                "modifiedAt": modified_at,
                "name": name,
                "parentStorageId": parent_storage_id,
                "schema": schema,
                "webURL": web_url,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Location":
        d = src_dict.copy()
        id = d.pop("id")

        barcode = d.pop("barcode")

        created_at = d.pop("createdAt")

        creator = UserSummary.from_dict(d.pop("creator"))

        fields = Fields.from_dict(d.pop("fields"))

        modified_at = d.pop("modifiedAt")

        name = d.pop("name")

        parent_storage_id = d.pop("parentStorageId")

        schema = SchemaSummary.from_dict(d.pop("schema"))

        web_url = d.pop("webURL")

        location = Location(
            id=id,
            barcode=barcode,
            created_at=created_at,
            creator=creator,
            fields=fields,
            modified_at=modified_at,
            name=name,
            parent_storage_id=parent_storage_id,
            schema=schema,
            web_url=web_url,
        )

        return location
