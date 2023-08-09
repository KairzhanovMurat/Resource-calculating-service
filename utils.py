def merge_results(data_1c: dict, data_micronic: dict) -> dict:
    merged_dict = {key: {'1C': data_1c[key], 'Micronic': data_micronic[key]} for key in data_1c}
    return merged_dict
