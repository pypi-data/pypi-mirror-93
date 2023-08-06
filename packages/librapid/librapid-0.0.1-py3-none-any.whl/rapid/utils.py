def _flatten(x, res):
    if type(x[0]) not in (list, tuple):
        res += x

    for val in x:
        if type(val) in (list, tuple):
            _flatten(val, res)

    return res

def flatten(x):
    return _flatten(x, [])
