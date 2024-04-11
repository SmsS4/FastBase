from dataclasses import dataclass
from typing import List, Optional

import dynaconf


@dataclass
class AppConfig:
    openapi_url: Optional[str] = None
    prefix: Optional[str] = None
    # DB
    db_host: Optional[str] = None
    db_port: Optional[str] = None
    db_name: Optional[str] = None
    db_username: Optional[str] = None
    db_password: Optional[str] = None

    cors_middleware: bool = False
    cors_allow_origins: Optional[List[str]] = None
    cors_allow_methods: Optional[List[str]] = None
    cors_allow_headers: Optional[List[str]] = None

    uvicorn_host: str = "localhost"
    uvicorn_port: int = 7000


def from_toml(paths: List[str]) -> AppConfig:
    settings = dynaconf.Dynaconf(
        envvar_prefix="FASE",
        settings_files=paths,
        environments=True,
        lowercase_read=False,
        load_dotenv=True,
        auto_cast=True,
    )
    extra = {}
    if "CORS" in settings.keys():
        extra.update(
            {
                "cors_middleware": True,
                "cors_allow_origins": settings.CORS.allow_origins,
                "cors_allow_methods": settings.CORS.allow_methods,
                "cors_allow_headers": settings.CORS.allow_headers,
            }
        )
    else:
        extra.update({"cors_middleware": False})
    if "UVICORN" in settings.keys():
        extra.update(
            {
                "uvicorn_host": settings.UVICORN.get("host", None),
                "uvicorn_port": settings.UVICORN.get("port", None),
            }
        )
    return AppConfig(
        openapi_url=settings.FASE.openapi_url,
        prefix=settings.FASE.prefix,
        db_host=settings.DB.host,
        db_port=settings.DB.port,
        db_name=settings.DB.name,
        db_username=settings.DB.username,
        db_password=settings.DB.password,
        **extra,
    )
