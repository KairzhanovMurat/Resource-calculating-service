import uvicorn
from fastapi import FastAPI, HTTPException, status, UploadFile, File, Request
from fastapi.templating import Jinja2Templates

import schemas
import services
import utils

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post('/select_calc')
async def optional_calculation(*, doc: UploadFile = File(...),
                               calc_type: schemas.CalculationType):
    items = await services.parse_excel(doc)
    micronic_data = services.get_remains()
    _1c_data = services.fetch_data_from_1c()
    if calc_type == schemas.CalculationType.one_unit:
        _1c_search = services.calculate_articuls_for_one(bom_items=items, search_items=_1c_data)
        micronic_search = services.calculate_articuls_for_one(bom_items=items, search_items=micronic_data)
        return utils.merge_results(_1c_search, micronic_search)
    elif calc_type == schemas.CalculationType.max_units_for_all_articuls:
        _1c_search = services.calculate_num_routers_for_articul(bom_items=items, search_items=_1c_data)
        micronic_search = services.calculate_num_routers_for_articul(bom_items=items, search_items=micronic_data)
        return utils.merge_results(_1c_search, micronic_search)
    elif calc_type == schemas.CalculationType.max_units_total:
        _1c_search = services.calculate_routers_total(bom_items=items, search_items=_1c_data)
        micronic_search = services.calculate_routers_total(bom_items=items, search_items=micronic_data)
        return {'макс. кол-во доступных роутеров': {'Micronic': micronic_search,
                                                    '1C': _1c_search}}
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                        detail='Unsupported calculation type')


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
