import uvicorn
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
import os
import services
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
static_path = os.path.join(os.path.dirname(__file__), 'static')


@app.get('/remains')
def remains():
    return services.get_remains()


@app.post('/calculate_routers_total')
async def calc(bom: UploadFile = File(...)):
    items = await services.parse_excel(bom)
    routers = services.calculate_routers_total(items)
    return {'num routers': routers}


@app.post('/calculate_max_routers')
async def calc_res(bom: UploadFile = File(...)):
    items = await services.parse_excel(bom)
    return services.calculate_num_routers_for_articul(items)


@app.post('/calculate_single_router')
async def calc_res(bom: UploadFile = File(...)):
    items = await services.parse_excel(bom)
    return services.calculate_articuls_for_one(items)


@app.post('/parse_data_1c')
async def parse(data: UploadFile = File(...)):
    return await services.fetch_data_from_1c(data)


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/show_tables", response_class=HTMLResponse)
async def show_tables(request: Request, bom: UploadFile = File(...)):
    items = await services.parse_excel(bom)
    routers_total = services.calculate_articuls_for_one(items)
    single_router = services.calculate_num_routers_for_articul(items)

    return templates.TemplateResponse(
        "tables.html",
        {"request": request, "routers_total": routers_total, "single_router": single_router},
    )


if __name__ == '__main__':
    uvicorn.run('main:app', host="0.0.0.0", port=8000, reload=True)
