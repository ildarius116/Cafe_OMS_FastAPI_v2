from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).parent.parent
DB_PATH = BASE_DIR / "cafe.db"
DB_TEST_PATH = BASE_DIR / "test_cafe.db"


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8000


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        # "api/v1/auth/login"
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class WebPrefix(BaseModel):
    prefix: str = ""


class DatabaseConfig(BaseModel):
    db_url: str = f"sqlite+aiosqlite:///{DB_PATH}"
    db_test_url: str = f"sqlite+aiosqlite:///{DB_TEST_PATH}"
    debug: bool = True
    echo: bool = False
    echo_pool: bool = False
    pool_size: int = 50
    max_overflow: int = 10

    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }


class AccessToken(BaseModel):
    lifetime_seconds: int = 3600
    reset_password_token_secret: str
    verification_token_secret: str


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(
            BASE_DIR / ".env.template",
            BASE_DIR / ".env",
        ),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="APP_CONFIG__",
    )

    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    web: WebPrefix = WebPrefix()
    db: DatabaseConfig
    access_token: AccessToken

    ORDER_STATUSES: dict = {
        "pending": "В ожидании",
        "ready": "Готово",
        "paid": "Оплачено",
    }

    MENU_ITEM_TYPES: dict = {
        "not assigned": "Не назначено",
        "first courses": "Первые блюда",
        "second courses": "Вторые блюда",
        "garnishes": "Гарниры",
        "salads": "Салаты",
        "desserts": "Десерты",
        "cold drinks": "Холодные напитки",
        "hot drinks": "Горячие напитки",
        "others": "Прочее",
    }


settings = Settings()
