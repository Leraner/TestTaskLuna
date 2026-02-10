from uuid import uuid4

from infrastructure.seeders.base_seeder import BaseSeeder
from src.activities.domain.entity import Activity
from src.activities.domain.ports.activity_repository import IActivityRepositoryPort


class ActivitySeeder(BaseSeeder):
    def __init__(self, activity_repository: IActivityRepositoryPort) -> None:
        self._activity_repository = activity_repository

    async def seed(self) -> None:
        existing_activities = await self._activity_repository.get_all()
        if existing_activities:
            return

        food = Activity(name="Еда", level=0, parent_id=None)
        await self._activity_repository.save(food)

        cars = Activity(name="Автомобили", level=0, parent_id=None)
        await self._activity_repository.save(cars)

        all_activities = await self._activity_repository.get_all()
        food_saved = next((a for a in all_activities if a.name == "Еда"), None)
        cars_saved = next((a for a in all_activities if a.name == "Автомобили"), None)

        if not food_saved or not cars_saved:
            return

        meat = Activity(name="Мясная продукция", parent_id=food_saved.id, level=1)
        await self._activity_repository.save(meat)

        dairy = Activity(name="Молочная продукция", parent_id=food_saved.id, level=1)
        await self._activity_repository.save(dairy)

        trucks = Activity(name="Грузовые", parent_id=cars_saved.id, level=1)
        await self._activity_repository.save(trucks)

        passenger = Activity(name="Легковые", parent_id=cars_saved.id, level=1)
        await self._activity_repository.save(passenger)

        all_activities = await self._activity_repository.get_all()
        passenger_saved = next((a for a in all_activities if a.name == "Легковые"), None)

        if not passenger_saved:
            return

        parts = Activity(name="Запчасти", parent_id=passenger_saved.id, level=2)
        await self._activity_repository.save(parts)

        accessories = Activity(name="Аксессуары", parent_id=passenger_saved.id, level=2)
        await self._activity_repository.save(accessories)

    async def clear(self) -> None:
        pass
