from uuid import uuid4

from infrastructure.seeders.base_seeder import BaseSeeder
from src.buildings.domain.entity import Building
from src.buildings.domain.ports.building_repository import IBuildingRepositoryPort
from src.shared_kernel.value_object import LatitudeVO, LongitudeVO


class BuildingSeeder(BaseSeeder):
    def __init__(self, building_repository: IBuildingRepositoryPort) -> None:
        self._building_repository = building_repository

    async def seed(self) -> None:
        existing_buildings = await self._building_repository.get_all()
        if existing_buildings:
            return

        buildings_data = [
            {
                "address": "г. Новосибирск, ул. Ленина, 1",
                "latitude": 55.030199,
                "longitude": 82.920430,
            },
            {
                "address": "г. Новосибирск, пр. Карла Маркса, 20",
                "latitude": 55.028874,
                "longitude": 82.927810,
            },
            {
                "address": "г. Новосибирск, ул. Красный проспект, 50",
                "latitude": 55.030204,
                "longitude": 82.920700,
            },
            {
                "address": "г. Москва, ул. Тверская, 10",
                "latitude": 55.761539,
                "longitude": 37.614810,
            },
            {
                "address": "г. Санкт-Петербург, Невский проспект, 28",
                "latitude": 59.934280,
                "longitude": 30.332260,
            },
        ]

        for data in buildings_data:
            building = Building(
                id=uuid4(),
                address=data["address"],
                latitude=LatitudeVO.from_value(data["latitude"]),
                longitude=LongitudeVO.from_value(data["longitude"]),
            )
            await self._building_repository.save(building)

    async def clear(self) -> None:
        pass
