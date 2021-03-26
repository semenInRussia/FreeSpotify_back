class FieldSerializer:
    serialize = None

    def __init__(self, field_name_for_serialize: str = None):
        self._field_name_for_serialize = field_name_for_serialize

    @property
    def field_name_for_serialize(self):
        return self._field_name_for_serialize

    @field_name_for_serialize.setter
    def field_name_for_serialize(self, value: str):
        print('OK')

        self._field_name_for_serialize = value

    def serialize_field_of(self, obj):
        not_serialized_value = getattr(obj, self.field_name_for_serialize)

        if not_serialized_value is None:
            return None

        return self.serialize(not_serialized_value)

    def has_not_field_name_for_serialize(self):
        return not bool(self.field_name_for_serialize)


class CustomFieldSerializer(FieldSerializer):
    def __init__(self, serialize_function, field_name_for_serializing: str = None):
        super().__init__(field_name_for_serializing)

        self.serialize = serialize_function


class StringFieldSerializer(FieldSerializer):
    serialize = str


class IntegerFieldSerializer(FieldSerializer):
    serialize = int


class FloatFieldSerializer(FieldSerializer):
    serialize = float


class BooleanFieldSerializer(FieldSerializer):
    serialize = bool


class ListFieldSerializer(FieldSerializer):
    serialize_elements_of_list = None

    def serialize(self, value):
        return list(map(
            self.serialize_elements_of_list, value
        ))


class CustomListFieldSerializer(ListFieldSerializer):
    def __init__(self, serialize_elements_of_list, field_name_for_serializing: str = None):
        self.serialize_elements_of_list = serialize_elements_of_list

        super().__init__(field_name_for_serializing)
