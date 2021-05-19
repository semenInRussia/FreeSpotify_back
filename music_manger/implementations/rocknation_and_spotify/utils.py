from collections import namedtuple

Brackets = namedtuple("Brackets", ["open_char", "closed_char"])


def delete_year_in_album_name(album_name: str) -> str:
    return album_name[7:]


def delete_sound_quality(name: str):
    brackets_types = [
        Brackets("(", ")"),
        Brackets("[", "]")
    ]
    res = name

    for brackets in brackets_types:
        res = _delete_value_in_brackets(res, brackets)

    return res


def _delete_value_in_brackets(name: str, brackets: Brackets):
    if _is_sound_quality_in_album_name(name, brackets):
        open_branch_index = name.find(brackets.open_char)
        closed_branch_index = name.find(brackets.closed_char) + 1

        space_before_branch_index = open_branch_index - 1

        brackets_and_value = name[space_before_branch_index: closed_branch_index]

        new_string = name.replace(brackets_and_value, "")

        return new_string
    else:
        return name


def _is_sound_quality_in_album_name(album_name: str, brackets: Brackets):
    return not _is_sound_quality_not_in_album_name(album_name, brackets)


def _is_sound_quality_not_in_album_name(album_name: str, brackets: Brackets):
    status_when_char_not_found: int = -1
    return album_name.find(brackets.open_char) == status_when_char_not_found
