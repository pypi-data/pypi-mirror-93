from typing import Any, Dict, Union, cast

import attr

from ..models.fields import Fields
from ..models.schema_summary import SchemaSummary
from ..models.user_summary import UserSummary
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AssayRun:
    """  """

    id: str
    schema: SchemaSummary
    fields: Fields
    project_id: Union[Unset, str] = UNSET
    created_at: Union[Unset, str] = UNSET
    creator: Union[UserSummary, Unset] = UNSET
    entry_id: Union[Unset, str] = UNSET
    is_reviewed: Union[Unset, bool] = UNSET
    validation_schema: Union[Unset, str] = UNSET
    validation_comment: Union[Unset, str] = UNSET
    api_url: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        schema = self.schema.to_dict()

        fields = self.fields.to_dict()

        project_id = self.project_id
        created_at = self.created_at
        creator: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.creator, Unset):
            creator = self.creator.to_dict()

        entry_id = self.entry_id
        is_reviewed = self.is_reviewed
        validation_schema = self.validation_schema
        validation_comment = self.validation_comment
        api_url = self.api_url

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "id": id,
                "schema": schema,
                "fields": fields,
            }
        )
        if project_id is not UNSET:
            field_dict["projectId"] = project_id
        if created_at is not UNSET:
            field_dict["createdAt"] = created_at
        if creator is not UNSET:
            field_dict["creator"] = creator
        if entry_id is not UNSET:
            field_dict["entryId"] = entry_id
        if is_reviewed is not UNSET:
            field_dict["isReviewed"] = is_reviewed
        if validation_schema is not UNSET:
            field_dict["validationSchema"] = validation_schema
        if validation_comment is not UNSET:
            field_dict["validationComment"] = validation_comment
        if api_url is not UNSET:
            field_dict["apiURL"] = api_url

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AssayRun":
        d = src_dict.copy()
        id = d.pop("id")

        schema = SchemaSummary.from_dict(d.pop("schema"))

        fields = Fields.from_dict(d.pop("fields"))

        project_id = d.pop("projectId", UNSET)

        created_at = d.pop("createdAt", UNSET)

        creator: Union[UserSummary, Unset] = UNSET
        _creator = d.pop("creator", UNSET)
        if _creator is not None and not isinstance(_creator, Unset):
            creator = UserSummary.from_dict(cast(Dict[str, Any], _creator))

        entry_id = d.pop("entryId", UNSET)

        is_reviewed = d.pop("isReviewed", UNSET)

        validation_schema = d.pop("validationSchema", UNSET)

        validation_comment = d.pop("validationComment", UNSET)

        api_url = d.pop("apiURL", UNSET)

        assay_run = AssayRun(
            id=id,
            schema=schema,
            fields=fields,
            project_id=project_id,
            created_at=created_at,
            creator=creator,
            entry_id=entry_id,
            is_reviewed=is_reviewed,
            validation_schema=validation_schema,
            validation_comment=validation_comment,
            api_url=api_url,
        )

        return assay_run
