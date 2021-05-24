from brackets_lib import delete_all_values_with_all_brackets


def delete_sound_quality(string: str) -> str:
    string = delete_all_values_with_all_brackets(string)

    return string.strip()

def delete_year_in_album_name(album_name: str) -> str:
    return album_name[7:]
