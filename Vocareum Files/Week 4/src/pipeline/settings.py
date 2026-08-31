from __future__ import annotations
from pathlib import Path
from pydantic import  BaseModel,Field
import time
from pydantic_settings import BaseSettings, SettingsConfigDict
#.env is in root directory i.e. week 4.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env" 
#modified the code in W3 to add the option of local LLM
class Settings(BaseSettings):
    """Runtime configuration. Validated at construction."""
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        extra="ignore",
    )
    questions_csv: Path  = Path("data/questions.csv")
    results_json:  Path  = Path("results.json")
    results_db:    Path  = Path("results.db")
    batch_size:    int   = Field(5,   gt=0, le=20)
    fail_rate:     float = Field(0.0, ge=0.0, le=1.0)
    model:         str   = "gpt-4o-mini"
    use_fake:      bool  = False
    # W4 LLM/retry configuration
    openai_api_key: str = ""
    openai_base_url: str = ""
    max_retries: int = Field(3, ge=0)
    retry_delay_s: float = Field(1.0, gt=0)




class RunSummary(BaseModel):
    """One row per pipeline execution. Persisted to the `runs` table."""

    started_at:       float
    elapsed_seconds:  float = Field(ge=0.0)
    n_questions:      int   = Field(ge=0)
    n_succeeded:      int   = Field(ge=0)
    n_retries_total:  int   = Field(ge=0)
    total_cost_usd:   float = Field(ge=0.0)
    fail_rate:        float = Field(ge=0.0, le=1.0)
    use_fake:         bool
