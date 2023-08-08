import uvicorn
from fastapi import FastAPI, HTTPException, status, UploadFile, File, Request
from typing import Dict
import schemas
import services
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")




@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/select_calc')
async def optional_calculation(*, doc: UploadFile = File(...),
                               calc_type: schemas.CalculationType):
    items = await services.parse_excel(doc)
    if calc_type == schemas.CalculationType.one_unit:
        return services.calculate_articuls_for_one(items)
    elif calc_type == schemas.CalculationType.max_units_for_all_articuls:
        return services.calculate_num_routers_for_articul(items)
    elif calc_type == schemas.CalculationType.max_units_total:
        return {'макс. кол-во доступных роутеров': f'{services.calculate_routers_total(items)}'}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                         detail='Unsupported calculation type')


# @app.get("/", response_class=HTMLResponse)
# async def read_item():
#     return templates.TemplateResponse("index.html", {"request": None, "result": None})
#
#
# @app.get('/remains')
# def remains():
#     return services.get_remains()
#
#
# @app.post('/parse_data_1c')
# async def parse(data: UploadFile = File(...)):
#     return await services.fetch_data_from_1c(data)


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
