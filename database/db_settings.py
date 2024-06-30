from os import environ
from string import Template
import logging


class DatabaseSettings:
    """
    Reads env data and configures string for configure sqlalchemy engine
    """

    CONNECT_STRING = Template("postgresql+asyncpg://${user}:${password}@${hostname}/${dbname}")

    USER_NAME = "SQL_USER"
    PASSWORD = "SQL_PASSWORD"
    HOSTNAME = "SQL_HOSTNAME"
    DBNAME = "SQL_DATABASE_NAME"

    @classmethod
    def get_url(cls) -> str:
        """
        returns a string url for configure sqlalchemy engine
        """

        logging.info("Read data from env for database")

        url= cls.CONNECT_STRING.substitute(
            user=environ.get(cls.USER_NAME),
            password=environ.get(cls.PASSWORD),
            hostname=environ.get(cls.HOSTNAME),
            dbname=environ.get(cls.DBNAME),
        )
        print(f"{url=}")
        return url
