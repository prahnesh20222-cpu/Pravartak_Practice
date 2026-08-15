from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    OPEN_AI_API_KEY:str 
    OPEN_AI_BASE_URL:str = "https://openai.vocareum.com/v1"
    OPEN_AI_RETRIES:int
    OPEN_AI_TEMPRATURE:float
    OPEN_AI_TIMEOUT:int

    model_config = SettingsConfigDict(
        env_file=".env",
    )

my_settings = Settings()