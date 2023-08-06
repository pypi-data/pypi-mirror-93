from fastapi import APIRouter

from .v2.views import router as v2
from .v1.views import router as v1

serving_route = APIRouter()

serving_route.include_router(v1)
serving_route.include_router(v2)
