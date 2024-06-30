from os import getenv


class Settings:
    ADMIN_ID = "ADMIN_ID"
    @classmethod
    def get_admin_id(cls) -> str:
        return getenv(cls.ADMIN_ID)
        