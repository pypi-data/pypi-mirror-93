from typing import Any, Dict

import attr

from ..models.measurement import Measurement


@attr.s(auto_attribs=True)
class ContainerContent:
    """  """

    concentration: Measurement

    def to_dict(self) -> Dict[str, Any]:
        concentration = self.concentration.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "concentration": concentration,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "ContainerContent":
        d = src_dict.copy()
        concentration = Measurement.from_dict(d.pop("concentration"))

        container_content = ContainerContent(
            concentration=concentration,
        )

        return container_content
