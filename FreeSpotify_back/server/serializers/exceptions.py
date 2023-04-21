class NotFoundSerializerError(Exception):
    """Serializer for a given type isn't found."""

class SerializerFieldNameNotProvidedError(Exception):
    """Try to serialize the field of an object, but the field name isn't provided."""
