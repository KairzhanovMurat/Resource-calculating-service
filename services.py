import io
from itertools import groupby
from decouple import config
import pandas as pd
import requests
from fastapi import UploadFile, File

url = config('ostatki_url')


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
    remains = requests.get(url).json()
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


def fetch_data_from_1c() -> dict:
    items = pd.read_excel('/home/murat/Downloads/СЭЗ остатки.xls')
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


def calculate_articuls_for_one(bom_items: dict, search_items: dict) -> dict:
    res_dict = dict()
    for articul in bom_items:
        if search_items.get(articul) is not None:
            difference = search_items[articul] - bom_items[articul]
            if difference < 0:
                res_dict[articul] = f'не хватает'
            else:
                res_dict[articul] = f' осталось {difference}, с учетом вычета'
        else:
            res_dict[articul] = f'отсутствует на складе'
    return res_dict


def calculate_routers_total(bom_items: dict, search_items: dict) -> int:
    routers_available = []
    for articul in bom_items:
        if search_items.get(articul) is not None:
            routers_max = search_items[articul] // bom_items[articul]
        else:
            return 0
        routers_available.append(routers_max)
    return min(routers_available)


def calculate_num_routers_for_articul(bom_items: dict, search_items: dict) -> dict:
    res_dict = dict()
    for articul in bom_items:
        if search_items.get(articul) is not None:
            routers_num = search_items[articul] // bom_items[articul]
            if routers_num >= 1:
                remainder = search_items[articul] % bom_items[articul]
                res_dict[articul] = f'хватит на {routers_num} роутеров, остаток: {remainder} шт.'
            else:
                res_dict[articul] = f'хватит на {routers_num} роутеров.'
        else:
            needed_amount = bom_items[articul]
            res_dict[articul] = f'отсутствует'
    return res_dict


def generate_doc(*args, **kwargs):
    ...
