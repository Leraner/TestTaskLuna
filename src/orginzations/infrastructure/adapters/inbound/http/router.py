from fastapi import APIRouter

from src.orginzations.infrastructure.adapters.inbound.http.get_organization_by_id.route import (
    route as get_organization_by_id_route,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_organizations.route import (
    route as get_organizations_route,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organization_by_name.route import (
    route as search_organization_by_name_route,
)
from src.orginzations.infrastructure.adapters.inbound.http.get_paginated_organizations_by_building_id.route import (
    route as get_paginated_organizations_by_building_id_route,
)
from src.orginzations.infrastructure.adapters.inbound.http.search_organizations_by_activity.route import (
    route as search_organizations_by_activity_route,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])

router.include_router(get_organization_by_id_route)
router.include_router(get_paginated_organizations_by_building_id_route)
router.include_router(search_organization_by_name_route)
router.include_router(search_organizations_by_activity_route)
router.include_router(get_organizations_route)
