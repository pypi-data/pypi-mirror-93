def split_params(param_str):
    dct = {}
    for param in param_str.split(';'):
        if not param:
            continue
        try:
            key, value = param.split('=', 1)
        except ValueError:
            continue
        dct[key] = value
    return dct
