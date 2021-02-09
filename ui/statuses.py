from typing import Union


class statuses:
    OK = "OK"
    FAIL = "FAIL"


class Status:
    _value = statuses.OK

    def __init__(self, status_name: str = None):
        if status_name is not None:
            self.set(status_name)

    def set(self, value: str):
        self._value = value

    @property
    def value(self):
        return self._value

    def __eq__(self, other: Union["Status", str]):
        status_class = self.__class__

        if isinstance(other, status_class):
            return other.value == self.value
        else:
            return other == self.value

    def __hash__(self):
        return hash(self.value)
