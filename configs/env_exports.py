from pydantic_settings import BaseSettings, SettingsConfigDict # type: ignore

class ENV_Exports(BaseSettings):
     mongodb_cluster_pass: str
     mongodb_cluster_un: str
     mongodb_cluster_db: str
     jwt_secret: str
     model_config = SettingsConfigDict(env_file=".env")

envs = ENV_Exports()