import requests
from fastapi import UploadFile, File
import pandas as pd


async def items_count(BOM: UploadFile = File(...)):
    file = await BOM.read()
    items = pd.read_excel(file)
    end = len(items) - 2
    names = items.iloc[9:end, 4]
    quantities = items.iloc[9:end, 14]
    return dict(zip(names, quantities))


async def fetch_data(*args, **kwargs):
    ...


def generate_doc(*args, **kwargs):
    ...


def calculate():
    pass
