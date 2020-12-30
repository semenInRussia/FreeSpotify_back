class Field:
    func = None

    def __init__(self, field_name: str):
        self._field_name = field_name

    def get_value(self, obj):
        field_value = getattr(obj, self._field_name)

        return self.func(field_value)


class CustomField(Field):
    def __init__(self, field_name: str, func):
        super().__init__(field_name)
        self.func = func


class StringField(Field):
    func = str


class IntegerField(Field):
    func = int


class FloatField(Field):
    func = float


class BooleanField(Field):
    func = bool
