def sum_of_lists(*lists):
    result = []

    for current_list in lists:
        result.extend(current_list)

    return result
