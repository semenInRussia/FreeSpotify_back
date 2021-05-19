from functools import lru_cache

cashed_function = lru_cache()


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
