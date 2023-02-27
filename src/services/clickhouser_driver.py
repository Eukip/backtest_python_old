import asyncio
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import asynch
from asynch import connect

from core.config import settings
from asynch.cursors import DictCursor

templates_folder = "jinja_templates"


def get_default_connect_settings():
    settings_base_dict = {
        "host": settings.CLICKHOUSE_HOST,
        "port": settings.CLICKHOUSE_PORT,
        "user": settings.CLICKHOUSE_USER,
        "password": settings.CLICKHOUSE_PASSWORD,
        "database": settings.CLICKHOUSE_DATABASE,
    }
    return settings_base_dict


def value_type_processing(value):
    if isinstance(value, datetime):
        value = value.strftime("%Y-%m-%d %H-%M-%S")
    if isinstance(value, (int, float)):
        return f"{value}"
    return f"'{value}'"


@dataclass
class ConnectSettings:
    host: str
    port: str
    user: str
    password: str
    database: str

    @classmethod
    def default(cls):
        return cls(**get_default_connect_settings())






class ClickHouseConnector:
    """
    Ассинхронный драйвер взаимодействия с кликхаусом
    """

    def __init__(self, connect_settings: ConnectSettings = None):
        if connect_settings:
            self.connect_settings = connect_settings
        else:
            self.connect_settings = ConnectSettings.default()
        self.conn = None

    async def _async_init(self):
        self.conn = await asynch.connect(
            host=self.connect_settings.host,
            port=self.connect_settings.port,
            user=self.connect_settings.user,
            password=self.connect_settings.password,
            database=self.connect_settings.database,
        )
        return self

    def __await__(self):
        # Async init
        return self._async_init().__await__()

    async def __aenter__(self):
        self.conn = await asynch.connect(
            host=self.connect_settings.host,
            port=self.connect_settings.port,
            user=self.connect_settings.user,
            password=self.connect_settings.password,
            database=self.connect_settings.database,
        )
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()


class SQLExecutor:
    @classmethod
    async def async_execute(
        cls,
        text_req,
        **kwargs,
    ):
        async with ClickHouseConnector(**kwargs) as ycl:
            async with ycl.cursor(cursor=DictCursor) as cursor:
                await cursor.execute(text_req)
                records = cursor.fetchall()
                return records

    @classmethod
    async def execute(connector: ClickHouseConnector, text_req):
        async with connector.conn.cursor(cursor=DictCursor) as cursor:
            await cursor.execute(text_req)
            records = cursor.fetchall()
            return records

    @classmethod
    async def async_insert(
        cls,
        text_req,
        data,
        **kwargs,
    ):

        async with ClickHouseConnector(**kwargs) as ycl:
            async with ycl.cursor(cursor=DictCursor) as cursor:
                res = await cursor.execute(text_req, data)
                return res


    @classmethod
    async def async_create(
        cls,
        text_req,
        **kwargs,
    ):
        conn = await connect(
            host=settings.CLICKHOUSE_HOST,
            port=settings.CLICKHOUSE_PORT,
            database=settings.CLICKHOUSE_DATABASE,
            user=settings.CLICKHOUSE_USER,
            password=settings.CLICKHOUSE_PASSWORD,
        )

        async with conn.cursor(cursor=DictCursor) as cursor:
            await cursor.execute(text_req)
            records = cursor.fetchall()
            return records
