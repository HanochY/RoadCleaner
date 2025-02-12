def validate_list_unique(l: list) -> list:
    if len(l) == len(set(l)):
        return l
    else:
        raise ValueError("List contains duplicates!")