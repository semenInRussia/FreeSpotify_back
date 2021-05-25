from brackets_lib import delete_all_values_with_all_brackets

name_on_year_splitter = " - "


def delete_sound_quality(string: str) -> str:
    string = delete_all_values_with_all_brackets(string).strip()

    name_and_year_with_sound_quality = string.split(name_on_year_splitter)

    if len(name_and_year_with_sound_quality) == 2:
        string, _ = name_and_year_with_sound_quality

    return string

def delete_year_in_album_name(album_name: str) -> str:
    return album_name[7:]
