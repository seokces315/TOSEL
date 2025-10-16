# GPT_Regular # 정기시험용
import os
from dotenv import load_dotenv

load_dotenv()

config = {
    "GPT_4o": {
        "generator": {
            "api_key": os.getenv("GPT_4o"),
            "model_id": "gpt-4o",
            "temperature": 0.7,
            "top_p": 0.9,
        },
        "parser": {
            "api_key": os.getenv("GPT_4o"),
            "model_id": "gpt-4o",
            "temperature": 0.7,
            "top_p": 0.9,
        },
    },
}
