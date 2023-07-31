from fastapi import HTTPException, status, APIRouter
import services
import services, schemas
_1c_router = APIRouter()


@_1c_router.get('/items')
async def get_items():
    items =  await services.fetch_data()
