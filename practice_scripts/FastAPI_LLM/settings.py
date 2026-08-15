from pydantic_settings import BaseSettings,SettingsConfigDict

'''
Create a settings class
Use the SettingsConfigDict to pass the env file path
'''
class Settings(BaseSettings):
    OPENAI_API_KEY: str
    OPENAI_BASE_URL: str = "https://openai.vocareum.com/v1"
    OPEN_AI_RETRIES: int
    OPEN_AI_TEMPERATURE: float
    model_config = SettingsConfigDict(
        env_file = ".env",
        
    )

'''
Create an instance of the of the Settings class
'''
my_settings = Settings()
