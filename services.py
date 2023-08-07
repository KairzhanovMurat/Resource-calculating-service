import io
from itertools import groupby

import pandas as pd
import requests
from fastapi import UploadFile, File


async def parse_excel(bom: UploadFile = File(...)) -> dict:
    content = await bom.read()
    with pd.ExcelFile(io.BytesIO(content)) as xls:
        sheet_name = xls.sheet_names[0]
        items = pd.read_excel(xls, sheet_name)
    end = len(items) - 2
    articuls = items.iloc[9:end, 3]
    quantities = items.iloc[9:end, 14]
    return dict(zip(articuls, quantities))


def get_remains() -> dict:
    # from collections import defaultdict
    remains = requests.get('http://10.10.2.180:5001/ostatki.json').json()
    dict_list = [{'articul': d['artukul'], 'quantity': int(d['quantity'])} for d in remains]
    # res_dict = defaultdict(int)
    # for dictionary in dict_list:
    #     articul = dictionary['articul']
    #     quantity = dictionary['quantity']
    #     res_dict[articul] += quantity
    # return dict(res_dict)
    dict_list.sort(key=lambda x: x['articul'])
    grouped_data = groupby(dict_list, key=lambda x: x['articul'])
    result_dict = {key: max(group, key=lambda x: x['quantity'])['quantity'] for key, group in grouped_data}
    return result_dict


def calculate_articuls_for_one(bom_items: dict) -> dict:
    remains = get_remains()
    for articul in bom_items:
        if remains.get(articul) is not None:
            difference = remains[articul] - bom_items[articul]
            if difference < 0:
                bom_items[articul] = f'не хватает, нужно дозаказать {abs(difference)} шт.'
            else:
                bom_items[articul] = f' осталось {difference}, с учетом вычета'
        else:
            bom_items[articul] = f'отсутствует на складе, нужно заказать {bom_items[articul]} шт'
    return bom_items


def calculate_routers_total(bom_items: dict) -> int:
    remains = get_remains()
    routers_available = []
    for articul in bom_items:
        if remains.get(articul) is not None:
            routers_max = remains[articul] // bom_items[articul]
        else:
            return 0
        routers_available.append(routers_max)
    return min(routers_available)


def calculate_num_routers_for_articul(items: dict) -> dict:
    remains = get_remains()
    for articul in items:
        if remains.get(articul) is not None:
            routers_num = remains[articul] // items[articul]
            if routers_num >= 1:
                remainder = remains[articul] % items[articul]
                items[articul] = f'хватит на {routers_num} роутеров, остаток: {remainder} шт.'
            else:
                items[articul] = f'хватит на {routers_num} роутеров.'
        else:
            needed_amount = items[articul]
            items[articul] = f'отсутствует, нужно заказать {needed_amount} шт.'
    return items


async def fetch_data_from_1c(data: UploadFile = File(...)) -> dict:
    content = await data.read()
    with pd.ExcelFile(io.BytesIO(content)) as xls:
        sheet_name = xls.sheet_names[0]
        items = pd.read_excel(xls, sheet_name)
    end = len(items) - 1
    articuls = items.iloc[15:end, 2]
    quantities = items.iloc[15:end, 8]
    payload = dict()
    for a, q in zip(articuls, quantities):
        if payload.get(a) is None:
            payload[a] = q
        else:
            payload[a] += q
    return payload


def generate_doc(*args, **kwargs):
    ...
