def get_cleaned_key(key: str):
    if "::" not in key:
        return key

    _, cleaned_key = key.split("::")
    return cleaned_key


def get_model_name(key: str):
    if "::" not in key:
        return None

    model_name, _ = key.split("::")
    return model_name
