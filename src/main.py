import sys
import uvicorn
from tortoise import Tortoise
from core.init_core import create_app
from core.config import settings
import logging


Tortoise.init_models(settings.APPS_MODELS, "models")


log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

app = create_app()

# json_logging.init_fastapi(enable_json=True)
# json_logging.init_request_instrument(app)

# logger = logging.getLogger("logger")
# logger.setLevel(logging.DEBUG)
# logger.addHandler(logging.StreamHandler(sys.stdout))


if __name__ == "__main__":
    uvicorn.run(app,
                #log_config=log_config,
                host=settings.host,
                port=settings.port)