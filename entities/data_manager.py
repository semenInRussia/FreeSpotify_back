class Serializer:
    all_fields = []

    def __init__(self, obj):
        self._object = obj


class DataManager:
    def __init__(self, obj, serializer):
        self._object = obj
        self._serializer: Serializer = serializer(obj)

    def get_serialized_data(self, *fields):
        data = {}

        if self._is_all_fields(fields):
            fields = self._serializer.all_fields

        for field in fields:
            data[field] = self._get_value(field)

        return data

    def _get_value(self, field: str):
        if hasattr(self._serializer, field):
            value = getattr(self._serializer, field)
        elif hasattr(self._object, field):
            value = getattr(self._object, field)
        else:
            raise AttributeError(f'key {field} is undefined')

        return value

    @staticmethod
    def _is_all_fields(fields: list):
        return len(fields) == 0 or fields[0] == "*"
