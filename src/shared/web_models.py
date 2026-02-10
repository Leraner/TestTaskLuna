from abc import abstractmethod

from pydantic import BaseModel, ConfigDict
from typing import Any


class BaseWebModel(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)


class BaseWebInputModel(BaseWebModel):
    """
    Базовая модель для входных данных веб-запросов.
    Все модели входных данных должны наследоваться от неё.
    """

    @abstractmethod
    def as_dto(self, *args, **kwargs) -> Any:
        """Метод отвечает за преобразование web-модели в DTO для дальнейшей передачи его в use-case."""
        ...


class BaseResponseDataModel(BaseWebModel):
    """
    Базовая модель данных, передаваемых в основной ответ на веб-запрос.
    Все модели данных ответа должны наследоваться от неё.
    Фактически является схемой для поля "data" в ответе.
    """

    def as_web_output(self):
        """Метод отвечает за преобразование модели данных ответа в модель ответа на веб-запрос."""
        return BaseWebOutputModel(data=self)


class PaginationData(BaseWebModel):
    total: int
    page: int
    page_size: int


class BaseWebOutputModel[
    ResponseData: BaseResponseDataModel | list[BaseResponseDataModel]
](BaseWebModel):
    """
    Базовая модель для данных ответа на веб-запрос.
    Для правильной работы необходимо указать модель данных ("data") в дженерике.
    """

    success: bool = True
    data: ResponseData | None = None
    error_code: str | None = None
    error_message: str | None = None


class PaginatedWebOutputModel[ItemModel: BaseResponseDataModel](BaseResponseDataModel):
    """
    Generic модель для пагинированных ответов на уровне presentation

    Использование:
        UserListWebOutputModel = PaginatedWebOutputModel[UserWebModel]
    """

    items: list[ItemModel]
    total_count: int
    page: int
    size: int

    def as_web_output(self):
        """Метод отвечает за преобразование пагинированных данных в модель ответа на веб-запрос."""
        return BaseWebOutputModel(data=self)
