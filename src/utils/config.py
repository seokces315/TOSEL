import os

from dotenv import load_dotenv
from dataclasses import dataclass

# Load environmental variables
load_dotenv()


@dataclass
class ModelConfig:
    api_key: str
    model_id: str
    temperature: float
    top_p: float


@dataclass
class ChainConfig:
    generator: ModelConfig
    parser: ModelConfig


# Function to get configuration objects for LLM chain
def get_chain_config(model_id):
    chain_config = ChainConfig(
        generator=ModelConfig(
            api_key=os.getenv("API_KEY"),
            model_id=model_id,
            temperature=0.7,
            top_p=0.9,
        ),
        parser=ModelConfig(
            api_key=os.getenv("API_KEY"),
            model_id=model_id,
            temperature=0.0,
            top_p=1.0,
        ),
    )

    return chain_config
