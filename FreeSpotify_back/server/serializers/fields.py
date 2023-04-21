from collections.abc import Callable, Iterable
from typing import Generic, Optional, TypeVar

from .exceptions import SerializerFieldNameNotProvidedError

I = TypeVar("I")                          # input field type
O = TypeVar("O")                          # output type

class FieldSerializer(Generic[I, O]):
    """A class to serialize a field of an object using certain function.

    Serialize function is a function that accept a serializable object and return
    other
    """

    serialize: Callable[[I], O]

    def __init__(self, field_name_to_serialize: Optional[str]=None):
        """Construct a serializer of a given field for any object.

        The serialization should be done with the `self.serialize` function.  Here's the
        main logic of this class.
        """
        self.field_name_to_serialize = field_name_to_serialize

    def serialize_field_of(self, obj: object) -> Optional[O]:
        """Apply this serializer to a given object."""
        if not self.field_name_to_serialize:
            raise SerializerFieldNameNotProvidedError

        raw_value: Optional[I] = getattr(obj, self.field_name_to_serialize)

        if raw_value is None:
            return None

        return self.serialize(raw_value)

    def has_not_field_name_to_serialize(self) -> bool:
        """Return True, if this field serializer don't know about the field name."""
        return not bool(self.field_name_to_serialize)


class CustomFieldSerializer(FieldSerializer):
    """Serializer of a field with a custom serialize function."""

    def __init__(self, serialize_function: Callable,
                 field_name_to_serialize: Optional[str] = None):
        """Create a field with a given name serializer with given serialzize func."""
        super().__init__(field_name_to_serialize)
        self.serialize = serialize_function


class StringFieldSerializer(FieldSerializer):
    """Serializer of a field with type int."""

    serialize = str


class IntegerFieldSerializer(FieldSerializer):
    """Serializer of a field with type int."""

    serialize = int


class FloatFieldSerializer(FieldSerializer):
    """Serializer of a field with type float."""

    serialize = float


class BooleanFieldSerializer(FieldSerializer):
    """Serializer of a field with type bool."""

    serialize = bool


I = TypeVar("I")                          # type of input list element
O = TypeVar("O")                          # type of output list element

class ListFieldSerializer(FieldSerializer, Generic[I, O]):
    """Serializer of a field with a composite list type."""

    serialize_element: Callable[[I], O]

    def serialize(self, obj: Iterable[I]) -> Iterable[O]:
        """Serialize a elements with 1st type to elements with 2nd type."""
        return map(self.serialize_element, obj)


class CustomListFieldSerializer(ListFieldSerializer):
    """Field serializer for list with custom serialize element function."""

    def __init__(self,
                 serialize_element: Callable,
                 field_name_to_serialize: Optional[str]=None):
        """Create a new field serializer with given function and name of the field."""
        self.serialize_element = serialize_element

        super().__init__(field_name_to_serialize)
