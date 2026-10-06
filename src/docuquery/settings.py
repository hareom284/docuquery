"""Config read from the environment — Laravel's config/ + .env, with types.

pydantic-settings is Pydantic with one extra trick: fields are filled from
environment variables (or a .env file) and validated like any other model.
Nothing else in the app reads os.environ.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Overridden by the DATABASE_URL env var — compose already sets it to the `db` host.
    database_url: str = "postgresql+psycopg://docuquery:docuquery@localhost:5432/docuquery"


settings = Settings()
