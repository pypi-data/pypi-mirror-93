import datetime
from typing import Any, Dict, List, Optional, Union, cast

import attr
from dateutil.parser import isoparse

from ..models.custom_fields import CustomFields
from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Entity:
    """  """

    aliases: Union[Unset, List[str]] = UNSET
    authors: Union[Unset, List[UserSummary]] = UNSET
    created_at: Union[Unset, datetime.datetime] = UNSET
    custom_fields: Union[CustomFields, Unset] = UNSET
    entity_registry_id: Union[Unset, Optional[str]] = UNSET
    fields: Union[Fields, Unset] = UNSET
    folder_id: Union[Unset, str] = UNSET
    id: Union[Unset, str] = UNSET
    modified_at: Union[Unset, datetime.datetime] = UNSET
    name: Union[Unset, str] = UNSET
    registry_id: Union[Unset, Optional[str]] = UNSET
    schema: Union[SchemaSummary, Unset] = UNSET
    web_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        aliases: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.aliases, Unset):
            aliases = self.aliases

        authors: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.authors, Unset):
            authors = []
            for authors_item_data in self.authors:
                authors_item = authors_item_data.to_dict()

                authors.append(authors_item)

        created_at: Union[Unset, str] = UNSET
        if not isinstance(self.created_at, Unset):
            created_at = self.created_at.isoformat()

        custom_fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.custom_fields, Unset):
            custom_fields = self.custom_fields.to_dict()

        entity_registry_id = self.entity_registry_id
        fields: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.fields, Unset):
            fields = self.fields.to_dict()

        folder_id = self.folder_id
        id = self.id
        modified_at: Union[Unset, str] = UNSET
        if not isinstance(self.modified_at, Unset):
            modified_at = self.modified_at.isoformat()

        name = self.name
        registry_id = self.registry_id
        schema: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.schema, Unset):
            schema = self.schema.to_dict()

        web_url = self.web_url

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if aliases is not UNSET:
            field_dict["aliases"] = aliases
        if authors is not UNSET:
            field_dict["authors"] = authors
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if custom_fields is not UNSET:
            field_dict["customFields"] = custom_fields
        if entity_registry_id is not UNSET:
            field_dict["entityRegistryId"] = entity_registry_id
        if fields is not UNSET:
            field_dict["fields"] = fields
        if folder_id is not UNSET:
            field_dict["folderId"] = folder_id
        if id is not UNSET:
            field_dict["id"] = id
        if modified_at is not UNSET:
            field_dict["modifiedAt"] = modified_at
        if name is not UNSET:
            field_dict["name"] = name
        if registry_id is not UNSET:
            field_dict["registryId"] = registry_id
        if schema is not UNSET:
            field_dict["schema"] = schema
        if web_url is not UNSET:
            field_dict["webURL"] = web_url

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Entity":
        d = src_dict.copy()
        aliases = cast(List[str], d.pop("aliases", UNSET))

        authors = []
        _authors = d.pop("authors", UNSET)
        for authors_item_data in _authors or []:
            authors_item = UserSummary.from_dict(authors_item_data)

            authors.append(authors_item)

        created_at = None
        _created_at = d.pop("createdAt", UNSET)
        if _created_at is not None:
            created_at = isoparse(cast(str, _created_at))

        custom_fields: Union[CustomFields, Unset] = UNSET
        _custom_fields = d.pop("customFields", UNSET)
        if _custom_fields is not None and not isinstance(_custom_fields, Unset):
            custom_fields = CustomFields.from_dict(cast(Dict[str, Any], _custom_fields))

        entity_registry_id = d.pop("entityRegistryId", UNSET)

        fields: Union[Fields, Unset] = UNSET
        _fields = d.pop("fields", UNSET)
        if _fields is not None and not isinstance(_fields, Unset):
            fields = Fields.from_dict(cast(Dict[str, Any], _fields))

        folder_id = d.pop("folderId", UNSET)

        id = d.pop("id", UNSET)

        modified_at = None
        _modified_at = d.pop("modifiedAt", UNSET)
        if _modified_at is not None:
            modified_at = isoparse(cast(str, _modified_at))

        name = d.pop("name", UNSET)

        registry_id = d.pop("registryId", UNSET)

        schema: Union[SchemaSummary, Unset] = UNSET
        _schema = d.pop("schema", UNSET)
        if _schema is not None and not isinstance(_schema, Unset):
            schema = SchemaSummary.from_dict(cast(Dict[str, Any], _schema))

        web_url = d.pop("webURL", UNSET)

        entity = Entity(
            aliases=aliases,
            authors=authors,
            created_at=created_at,
            custom_fields=custom_fields,
            entity_registry_id=entity_registry_id,
            fields=fields,
            folder_id=folder_id,
            id=id,
            modified_at=modified_at,
            name=name,
            registry_id=registry_id,
            schema=schema,
            web_url=web_url,
        )

        return entity
