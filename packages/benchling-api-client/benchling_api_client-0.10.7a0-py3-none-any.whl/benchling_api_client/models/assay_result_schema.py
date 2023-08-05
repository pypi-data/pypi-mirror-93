from typing import Any, Dict, List, Union

import attr

from ..models.assay_result_schema_archive_record import AssayResultSchemaArchiveRecord
from ..models.assay_result_schema_organization import AssayResultSchemaOrganization
from ..models.assay_result_schema_type import AssayResultSchemaType
from ..models.schema_field import SchemaField
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AssayResultSchema:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    archive_record: Union[Unset, None, AssayResultSchemaArchiveRecord] = UNSET
    field_definitions: Union[Unset, List[SchemaField]] = UNSET
    type: Union[Unset, AssayResultSchemaType] = UNSET
    system_name: Union[Unset, str] = UNSET
    derived_from: Union[Unset, None, str] = UNSET
    organization: Union[Unset, AssayResultSchemaOrganization] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        archive_record: Union[Unset, None, Dict[str, Any]] = UNSET
        if not isinstance(self.archive_record, Unset):
            archive_record = self.archive_record.to_dict() if self.archive_record else None

        field_definitions: Union[Unset, List[Any]] = UNSET
        if not isinstance(self.field_definitions, Unset):
            field_definitions = []
            for field_definitions_item_data in self.field_definitions:
                field_definitions_item = field_definitions_item_data.to_dict()

                field_definitions.append(field_definitions_item)

        type: Union[Unset, int] = UNSET
        if not isinstance(self.type, Unset):
            type = self.type.value

        system_name = self.system_name
        derived_from = self.derived_from
        organization: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.organization, Unset):
            organization = self.organization.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if archive_record is not UNSET:
            field_dict["archiveRecord"] = archive_record
        if field_definitions is not UNSET:
            field_dict["fieldDefinitions"] = field_definitions
        if type is not UNSET:
            field_dict["type"] = type
        if system_name is not UNSET:
            field_dict["systemName"] = system_name
        if derived_from is not UNSET:
            field_dict["derivedFrom"] = derived_from
        if organization is not UNSET:
            field_dict["organization"] = organization

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayResultSchema":
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        archive_record = None
        _archive_record = d.pop("archiveRecord", UNSET)
        if _archive_record is not None and not isinstance(_archive_record, Unset):
            archive_record = AssayResultSchemaArchiveRecord.from_dict(_archive_record)

        field_definitions = []
        _field_definitions = d.pop("fieldDefinitions", UNSET)
        for field_definitions_item_data in _field_definitions or []:
            field_definitions_item = SchemaField.from_dict(field_definitions_item_data)

            field_definitions.append(field_definitions_item)

        type = None
        _type = d.pop("type", UNSET)
        if _type is not None:
            type = AssayResultSchemaType(_type)

        system_name = d.pop("systemName", UNSET)

        derived_from = d.pop("derivedFrom", UNSET)

        organization: Union[Unset, AssayResultSchemaOrganization] = UNSET
        _organization = d.pop("organization", UNSET)
        if not isinstance(_organization, Unset):
            organization = AssayResultSchemaOrganization.from_dict(_organization)

        assay_result_schema = AssayResultSchema(
            id=id,
            name=name,
            archive_record=archive_record,
            field_definitions=field_definitions,
            type=type,
            system_name=system_name,
            derived_from=derived_from,
            organization=organization,
        )

        return assay_result_schema
