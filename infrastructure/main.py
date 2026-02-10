# from logging import config

import uvicorn

from infrastructure.web.settings import get_api_settings
from infrastructure.web.web_app import WebApplication

if __name__ == "__main__":
    settings = get_api_settings()
    # config.dictConfig(get_logging_config(settings=settings))

    application = WebApplication(settings=settings)
    uvicorn.run(
        app=application.create_application(),
        host=settings.host,
        port=settings.port,
    )
