from typing import Type

from FreeSpotify_back._low_level_utils import get_public_fields_of
from .fields import FieldSerializer


class Serializer:
    public_fields = ["all_fields", "object_type", "get_data", "public_fields"]

    all_fields: list[str] = []
    object_type = None

    def __init__(self, obj):
        self._obj = obj

    def get_data(self, *fields_for_serialize) -> dict:
        if self._is_all_fields(fields_for_serialize):
            fields_for_serialize = self._all_fields

        return self._serialize_object(fields_for_serialize)

    def _is_all_fields(self, fields) -> bool:
        return (self._all_fields == fields) or (not fields)

    @property
    def _all_fields(self):
        if not self.all_fields:
            self.all_fields = get_public_fields_of(self, ignore=self.public_fields)

        return self.all_fields

    def _serialize_object(self, fields) -> dict:
        return {
            field_name: self._serialize_field_by_name(field_name)
            for field_name in fields
        }

    def _serialize_field_by_name(self, field_for_serialize: str):
        field_serializer = self._get_field_serializer_for(field_for_serialize)

        return field_serializer.serialize_field_of(self._obj)

    def _get_field_serializer_for(self, field_name_for_serialize: str) -> FieldSerializer:
        field_serializer = getattr(self, field_name_for_serialize)

        if field_serializer.has_not_field_name_for_serialize():
            field_serializer.field_name_for_serialize = field_name_for_serialize

        return field_serializer


class GeneralSerializer(Serializer):
    all_serializers: list[Type[Serializer]] = []

    def get_data(self, *fields):
        serializer = self._get_current_serializer()

        return serializer(self._obj).get_data(*fields)

    def _get_current_serializer(self):
        current_obj_type = type(self._obj)

        for serializer in self.all_serializers:
            if serializer.object_type == current_obj_type:
                return serializer
