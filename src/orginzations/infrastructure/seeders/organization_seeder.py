from infrastructure.seeders.base_seeder import BaseSeeder
from src.orginzations.domain.entity import Organization
from src.orginzations.domain.ports.activity_access_port import IActivityAccessPort
from src.orginzations.domain.ports.building_access_port import IBuildingAccessPort
from src.orginzations.domain.ports.organization_repository import (
    IOrganizationRepositoryPort,
)
from src.orginzations.domain.value_objects import PhoneNumberVO


class OrganizationSeeder(BaseSeeder):
    def __init__(
        self,
        organization_repository: IOrganizationRepositoryPort,
        building_access_port: IBuildingAccessPort,
        activity_access_port: IActivityAccessPort,
    ) -> None:
        self._organization_repository = organization_repository
        self._building_access_port = building_access_port
        self._activity_access_port = activity_access_port

    async def seed(self) -> None:
        existing_orgs, _ = await self._organization_repository.search_by_name_paginated(
            page=1, size=1, organization_name=""
        )
        if existing_orgs:
            return

        buildings = await self._building_access_port.get_all_buildings()
        if not buildings:
            return

        activities = await self._activity_access_port.get_all_activities()
        if not activities:
            return

        activity_map = {act.name: act for act in activities}

        organizations_data = [
            {
                "name": "ООО Рога и Копыта",
                "phone_number": "+7-923-666-13-13",
                "building_index": 0,
                "activity_names": ["Еда", "Мясная продукция"],
            },
            {
                "name": "Молочный завод Простоквашино",
                "phone_number": "+7-923-123-45-67",
                "building_index": 0,
                "activity_names": ["Молочная продукция"],
            },
            {
                "name": "Автосалон Премиум",
                "phone_number": "+7-923-777-88-99",
                "building_index": 1,
                "activity_names": ["Автомобили", "Легковые"],
            },
            {
                "name": "Грузовик Транс",
                "phone_number": "+7-923-222-33-44",
                "building_index": 2,
                "activity_names": ["Грузовые"],
            },
            {
                "name": "Автозапчасти Плюс",
                "phone_number": "+7-923-555-66-77",
                "building_index": 2,
                "activity_names": ["Запчасти", "Аксессуары"],
            },
            {
                "name": "Ресторан У Ашота",
                "phone_number": "+7-495-111-22-33",
                "building_index": 3,
                "activity_names": ["Еда"],
            },
            {
                "name": "Автомойка Блеск",
                "phone_number": "+7-812-444-55-66",
                "building_index": 4,
                "activity_names": ["Автомобили"],
            },
        ]

        for data in organizations_data:
            if data["building_index"] >= len(buildings):
                continue

            building = buildings[data["building_index"]]

            activity_refs = [
                activity_map[name]
                for name in data["activity_names"]
                if name in activity_map
            ]

            organization = Organization(
                name=data["name"],
                phone_number=PhoneNumberVO.from_value(data["phone_number"]),
                building=building,
                activities=activity_refs,
            )
            await self._organization_repository.save(organization)

    async def clear(self) -> None:
        pass
