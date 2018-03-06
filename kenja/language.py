extension_dict = {'java': ['.java']}


def is_target_blob(blob):
    if not blob:
        return False

    for exts in extension_dict.values():
        for ext in exts:
            if blob.name.lower().endswith(ext):
                return True
    return False
