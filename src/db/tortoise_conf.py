from core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URL},
    "apps": {
        "models": {
            "models": settings.APPS_MODELS,
            "default_connection": "default",
        },
    },
}