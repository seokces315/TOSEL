import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environmental variables
load_dotenv()


# Pydantic class
class GeneratorConfig(BaseSettings):
    api_key: str
    model_id: str
    temperature: float
    top_p: float

    class Config:
        env_prefix = "GENERATOR_"


class ParserConfig(BaseSettings):
    api_key: str
    model_id: str
    temperature: float
    top_p: float

    class Config:
        env_prefix = "PARSER_"


class ChainConfig(BaseSettings):
    generator: GeneratorConfig
    parser: ParserConfig
