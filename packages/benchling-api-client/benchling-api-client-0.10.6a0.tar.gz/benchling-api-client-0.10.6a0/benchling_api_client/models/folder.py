from typing import Any, Dict, Union

import attr

from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class Folder:
    """  """

    id: Union[Unset, str] = UNSET
    name: Union[Unset, str] = UNSET
    parent_folder_id: Union[Unset, str] = UNSET
    project_id: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        id = self.id
        name = self.name
        parent_folder_id = self.parent_folder_id
        project_id = self.project_id

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if id is not UNSET:
            field_dict["id"] = id
        if name is not UNSET:
            field_dict["name"] = name
        if parent_folder_id is not UNSET:
            field_dict["parentFolderId"] = parent_folder_id
        if project_id is not UNSET:
            field_dict["projectId"] = project_id

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "Folder":
        d = src_dict.copy()
        id = d.pop("id", UNSET)

        name = d.pop("name", UNSET)

        parent_folder_id = d.pop("parentFolderId", UNSET)

        project_id = d.pop("projectId", UNSET)

        folder = Folder(
            id=id,
            name=name,
            parent_folder_id=parent_folder_id,
            project_id=project_id,
        )

        return folder
