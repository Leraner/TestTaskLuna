from fastapi import APIRouter

from src.buildings.infrastructure.adapters.inbound.http.get_paginated_buildings.route import (
    route as get_paginated_buildings_route,
)

route = APIRouter(prefix="/buildings", tags=["buildings"])

route.include_router(get_paginated_buildings_route)
