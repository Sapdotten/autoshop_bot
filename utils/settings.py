from os import environ


class Settings:
    ADMIN_ID = "ADMIN_ID"
    @classmethod
    def get_admin_id(cls) -> str:
        return environ.get(cls.ADMIN_ID)
        