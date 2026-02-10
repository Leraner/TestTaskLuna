class InfrastructureError(Exception):
    """Base infrastructure error"""

    detail = "Unknown error"
    ru_detail = "Неизвестная ошибка"
    extra: dict | None = None

    def __init__(
        self,
        detail: str | None = None,
        ru_detail: str | None = None,
        original_error: Exception | None = None,
        **kwargs,
    ):
        self.detail = self.detail if not detail else detail
        self.ru_detail = self.ru_detail if not ru_detail else ru_detail
        self.original_error = original_error
        self.extra = self.extra if not kwargs else kwargs
        super().__init__(self.detail)


class DatabaseError(InfrastructureError):
    pass
