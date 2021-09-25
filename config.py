from pydantic import BaseSettings, PostgresDsn


class BotConfig(BaseSettings):
    db_uri: PostgresDsn
    prefix: str
    server_id: int
    bot_token: str
    invite_req: int
    invite_role: int
    send_welcome: bool

    class Config:
        env_file = ".env"
        fields = {
            "database_uri": {"env": ["database_uri", "database_url", "database"]},
            "no_ssl": {"env": "database_no_ssl"},
            "secret": {"env": "signing_secret"},
        }


bot_config = BotConfig()
