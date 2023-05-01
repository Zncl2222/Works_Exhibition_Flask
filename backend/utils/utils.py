def array_to_string_encoder(array: list):
    res = {}
    for i in range(len(array)):
        res[i] = ', '.join(str(x) for x in array[i, :])

    return res


def array_to_string_decoder(data: dict):
    res = []
    for i in range(len(data)):
        str_list = data[i].split(',')
        float_list = [float(x) for x in str_list]
        res.append(float_list)

    return res
