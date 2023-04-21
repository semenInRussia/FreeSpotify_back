
from typing import Optional

from FreeSpotify_back._low_level_utils import first_true, get_public_fields_of

from .exceptions import NotFoundSerializerError
from .fields import FieldSerializer


class Serializer:
    """The serializer of certain object type to dict."""

    public_fields = ["all_fields", "object_type", "get_data", "public_fields"]

    all_fields: list[str] = []
    object_type = None

    def __init__(self, obj: object):
        """Pass object to future convert into serializer."""
        self._obj = obj

    def get_data(self, *fields_to_serialize: str) -> dict:
        """Convert a passed object to dict with given fields."""
        fields = list(fields_to_serialize)
        if self._is_all_fields(fields):
            fields = self._all_fields
        return self._serialize_object(fields)

    def _is_all_fields(self, fields: Optional[list[str]]) -> bool:
        return (self._all_fields == fields) or (not fields)

    @property
    def _all_fields(self) -> list[str]:
        if not self.all_fields:
            self.all_fields = get_public_fields_of(self,
                                                   ignore_list=self.public_fields)
        return self.all_fields

    def _serialize_object(self, fields: list[str]) -> dict:
        return {
            field_name: self._serialize_field_by_name(field_name)
            for field_name in fields
        }

    def _serialize_field_by_name(self, field_to_serialize: str):  # noqa: ANN202
        field_serializer = self._get_field_serializer_for(field_to_serialize)
        return field_serializer.serialize_field_of(self._obj)

    def _get_field_serializer_for(self,
                                  field_name_to_serialize: str) -> FieldSerializer:
        field_serializer: FieldSerializer = getattr(self, field_name_to_serialize)

        if field_serializer.has_not_field_name_to_serialize():
            field_serializer.field_name_to_serialize = field_name_to_serialize

        return field_serializer


class GeneralSerializer(Serializer):
    """Serializer to dict, it contains some serializers so it can convert some types."""

    all_serializers: list[type[Serializer]] = []

    def get_data(self, *fields: str) -> dict:
        """Convert a passed object to dict with given fields."""
        serializer = self._get_current_serializer()
        return serializer(self._obj).get_data(*fields)

    def _get_current_serializer(self) -> type[Serializer]:
        current_obj_type = type(self._obj)

        current_serializer = first_true(
            self.all_serializers,
            pred=lambda ser: ser.object_type == current_obj_type)

        if not current_serializer:
            raise NotFoundSerializerError

        return current_serializer
