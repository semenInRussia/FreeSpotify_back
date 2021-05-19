from functools import lru_cache

cashed_function = lru_cache()


def format_exception(error_name: str, error_description: str) -> str:
    if error_description:
        error_description = f"Description - \"{error_description}\""
    else:
        error_description = "Description not found..."

    return (
        f"Sorry... I'm found error...\n"
        "Detail:\n"
        f"|     Name - {error_name}\n"
        f"|     {error_description}"
    )


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
