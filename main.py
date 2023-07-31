from fastapi import FastAPI, File, UploadFile
import pandas as pd

app = FastAPI(docs_url='/')


@app.post('/BOM')
async def items_count(BOM: UploadFile = File(...)):
    file = await BOM.read()
    items = pd.read_excel(file)
    end = len(items) - 2
    articuls = items.iloc[9:end, 3]
    quantities = items.iloc[9:end, 14]
    return dict(zip(articuls, quantities))
