from typing import Any, Dict, List

import attr

from ..models.plate_schema import PlateSchema


@attr.s(auto_attribs=True)
class PlateSchemasPaginatedList:
    """  """

    next_token: str
    plate_schemas: List[PlateSchema]

    def to_dict(self) -> Dict[str, Any]:
        next_token = self.next_token
        plate_schemas = []
        for plate_schemas_item_data in self.plate_schemas:
            plate_schemas_item = plate_schemas_item_data.to_dict()

            plate_schemas.append(plate_schemas_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {
                "nextToken": next_token,
                "plateSchemas": plate_schemas,
            }
        )

        return field_dict

    @staticmethod
    def from_dict(src_dict: Dict[str, Any]) -> "PlateSchemasPaginatedList":
        d = src_dict.copy()
        next_token = d.pop("nextToken")

        plate_schemas = []
        _plate_schemas = d.pop("plateSchemas")
        for plate_schemas_item_data in _plate_schemas:
            plate_schemas_item = PlateSchema.from_dict(plate_schemas_item_data)

            plate_schemas.append(plate_schemas_item)

        plate_schemas_paginated_list = PlateSchemasPaginatedList(
            next_token=next_token,
            plate_schemas=plate_schemas,
        )

        return plate_schemas_paginated_list
