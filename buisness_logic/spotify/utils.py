def delete_sound_quality(album_name: str):
    if _is_sound_quality_in_album_name(album_name):
        branch_index = album_name.find("(")
        space_before_branch = branch_index - 1

        new_string = album_name[:space_before_branch]

        return new_string
    else:
        return album_name


def _is_sound_quality_in_album_name(album_name: str):
    return not _is_sound_quality_not_in_album_name(album_name)


def _is_sound_quality_not_in_album_name(album_name: str):
    status_when_char_not_found: int = -1
    return album_name.find("(") == status_when_char_not_found
