from typing import Union


class Serializer:
    all_fields = []
    obj_type = None

    def __init__(self, obj):
        self._obj = obj

    def get_data(self, *fields) -> Union[dict, list]:
        data = {}

        if self._is_all_fields(fields):
            fields = self.all_fields

        for field_name in fields:
            data[field_name] = self._get_field_value_by_name(field_name)

        return data

    @staticmethod
    def _is_all_fields(fields) -> bool:
        return bool(not fields)

    def _get_field_value_by_name(self, field_name):
        field = getattr(self, field_name)
        return field.get_value(self._obj)


class GeneralSerializer(Serializer):
    all_serializers = []

    def get_data(self, *fields):
        serializer = self._get_current_serializer()

        return serializer(self._obj).get_data(*fields)

    def _get_current_serializer(self):
        current_obj_type = type(self._obj)

        for serializer in self.all_serializers:
            if serializer.obj_type == current_obj_type:
                return serializer
