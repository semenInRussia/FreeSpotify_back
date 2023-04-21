from FreeSpotify_back.brackets_lib import delete_all_values_with_all_brackets_types

name_and_year_splitter = " - "

# len of "1984 - ", for example
len_of_year_with_splitter = 4 + len(name_and_year_splitter)


def delete_sound_quality(string: str) -> str:
    string = delete_all_values_with_all_brackets_types(string).strip()

    name_and_year_with_sound_quality = string.split(name_and_year_splitter)

    if len(name_and_year_with_sound_quality) >= 2:
        string, *_ = name_and_year_with_sound_quality

    return string

def delete_year_in_album_name(album_name: str) -> str:
    return album_name[7:]
