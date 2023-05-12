from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class CoreConfig:
    # DB config
    db_driver: str
    db_user: str
    db_password: str
    db_host: str
    db_name: str

    # Cache config
