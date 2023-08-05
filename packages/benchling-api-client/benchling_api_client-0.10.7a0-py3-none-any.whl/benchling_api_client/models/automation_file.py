from typing import Any, Dict, Union

import attr

from ..models.automation_file_automation_file_config import AutomationFileAutomationFileConfig
from ..models.automation_file_file import AutomationFileFile
from ..types import UNSET, Unset


@attr.s(auto_attribs=True)
class AutomationFile:
    """  """

    assay_run_id: Union[Unset, str] = UNSET
    automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
    file: Union[Unset, AutomationFileFile] = UNSET
    id: Union[Unset, str] = UNSET
    status: Union[Unset, str] = UNSET

    def to_dict(self) -> Dict[str, Any]:
        assay_run_id = self.assay_run_id
        automation_file_config: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.automation_file_config, Unset):
            automation_file_config = self.automation_file_config.to_dict()

        file: Union[Unset, Dict[str, Any]] = UNSET
        if not isinstance(self.file, Unset):
            file = self.file.to_dict()

        id = self.id
        status = self.status

        field_dict: Dict[str, Any] = {}
        field_dict.update({})
        if assay_run_id is not UNSET:
            field_dict["assayRunId"] = assay_run_id
        if automation_file_config is not UNSET:
            field_dict["automationFileConfig"] = automation_file_config
        if file is not UNSET:
            field_dict["file"] = file
        if id is not UNSET:
            field_dict["id"] = id
        if status is not UNSET:
            field_dict["status"] = status

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "AutomationFile":
        d = src_dict.copy()
        assay_run_id = d.pop("assayRunId", UNSET)

        automation_file_config: Union[Unset, AutomationFileAutomationFileConfig] = UNSET
        _automation_file_config = d.pop("automationFileConfig", UNSET)
        if not isinstance(_automation_file_config, Unset):
            automation_file_config = AutomationFileAutomationFileConfig.from_dict(_automation_file_config)

        file: Union[Unset, AutomationFileFile] = UNSET
        _file = d.pop("file", UNSET)
        if not isinstance(_file, Unset):
            file = AutomationFileFile.from_dict(_file)

        id = d.pop("id", UNSET)

        status = d.pop("status", UNSET)

        automation_file = AutomationFile(
            assay_run_id=assay_run_id,
            automation_file_config=automation_file_config,
            file=file,
            id=id,
            status=status,
        )

        return automation_file
