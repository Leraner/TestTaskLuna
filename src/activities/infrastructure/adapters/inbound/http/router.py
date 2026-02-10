from fastapi import APIRouter

from src.activities.infrastructure.adapters.inbound.http.get_paginated_activities.route import (
    route as get_paginated_activities_route,
)

router = APIRouter(prefix="/activities", tags=["activities"])

router.include_router(get_paginated_activities_route)

