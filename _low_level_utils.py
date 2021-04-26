def sum_of_lists(*lists):
    result = []

    for current_list in lists:
        result.extend(current_list)

    return result


def get_public_fields_of(obj, ignore=None):
    if ignore is None:
        ignore = []

    all_fields = dir(obj)
    is_public_field_name = lambda field_name: not (field_name.startswith("_") or field_name in ignore)

    return list(filter(
        is_public_field_name,

        all_fields
    ))


class Cash:
    def __init__(self, default_values=None):
        if default_values is None:
            default_values = []

        self._values = default_values

    def set(self, key, value):
        self._values[key] = value

    def get(self, key, func_return_result_if_undefined=None):
        if func_return_result_if_undefined is None:
            func_return_result_if_undefined = lambda current_key: None

        found_key = self._values.get(key)

        if found_key:
            return found_key
        else:
            return func_return_result_if_undefined(key)
