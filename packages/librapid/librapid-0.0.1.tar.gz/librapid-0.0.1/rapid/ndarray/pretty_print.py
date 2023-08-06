import math

def formatFloat(val, maxLength):
    val = float(val)

    if abs(val) < 1:
        maxLength -= 2

    if len(str(val)) <= maxLength:
        res = str(val)
    else:
        res = "{}:.{}{}".format("{", maxLength, "}")
        res = res.format(val)

    if res[-2:] == ".0":
        res = res[:-1]

    return res, (res.find(".") if "." in res else len(res))

# Convert a 1D list into an array with a given shape
def _1dToArr(data, shape, index):
    if len(shape) == 1:
        res = [data[i] for i in range(index, index + shape[0])]
        index += shape[0]
    else:
        res = []
        tmpIndex = index
        for i in range(shape[0]):
            tmpRes, tmpIndex = _1dToArr(data, shape[1:], tmpIndex)
            res.append(tmpRes)
        index = tmpIndex
   
    return res, index

def _array1dToString(arr, stripMiddle):
    res = "["
    i = 0
    # for i in range(len(arr)):
    while i < len(arr):
        if stripMiddle and len(arr) > 6 and i == 3:
            i = len(arr) - 3
            res += "... "

        res += arr[i]

        if i + 1 < len(arr):
            res += " "

        i += 1
    return res + "]"

def _arrayToString(data, shape, depth, stripMiddle):
    if len(shape) == 1:
        return _array1dToString(data, stripMiddle)
    elif len(shape) == 2:
        res = "["

        i = 0
        while i < len(data):
            if stripMiddle and shape[0] > 6 and i == 3:
                i = shape[0] - 3
                res += (" " * depth) + "...\n"

            if i != 0:
                res += " " * depth

            res += _array1dToString(data[i], stripMiddle)

            if i + 1 != len(data):
                res += "\n"

            i += 1

        return res + "]"
    else:
        res = "["

        i = 0
        while i < len(data):
            if stripMiddle and shape[0] > 6 and i == 3:
                i = shape[0] - 3
                res += (" " * depth) + "...\n\n"

            if i != 0:
                res += " " * depth
            
            res += _arrayToString(data[i], shape[1:], depth + 1, stripMiddle)

            if i + 1 < len(data):
                res += "\n\n"

            i += 1

        return res + "]"

def arrayToString(data, shape, dtype=None, startingDepth=1):
    if dtype == "float32":
        roundTo = 7
    elif dtype == "float64":
        roundTo = 15
    else:
        roundTo = 20

    formatted = [formatFloat(val, roundTo) for val in data]
    longestIntegeral = max([p for _, p in formatted])
    longestDecimal = max([len(n) - p - 1 for n, p in formatted])
    adjusted = []

    for term in formatted:
        n, integral = term
        decimal = len(n) - integral - 1
        tmp = (" " * (longestIntegeral - integral)) + n + (" " * (longestDecimal - decimal))
        adjusted.append(tmp)

    arr, _= _1dToArr(adjusted, shape, 0)

    # General check
    if math.prod(shape) > 1000:
        stripMiddle = True
    else:
        stripMiddle = False
    
    # Edge case
    if len(shape) == 2 and shape[1] == 1:
        stripMiddle = False

    res = _arrayToString(arr, shape, startingDepth, stripMiddle)
    return res
