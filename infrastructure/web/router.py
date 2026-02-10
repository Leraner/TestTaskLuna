from fastapi import APIRouter

from src.orginzations.infrastructure.adapters.inbound.http.router import (
    router as organizations_router,
)
from src.buildings.infrastructure.adapters.inbound.http.router import (
    route as buildings_router,
)
from src.activities.infrastructure.adapters.inbound.http.router import (
    router as activities_router,
)

router = APIRouter()

router.include_router(organizations_router)
router.include_router(buildings_router)
router.include_router(activities_router)