from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

from dataclasses import dataclass


# Function to generate LLM parser
def generate_llm_parser(chain_config):
    # Create generator object
    llm_parser = ChatOpenAI(
        openai_api_key=chain_config.parser.api_key,
        model=chain_config.parser.model_id,
        temperature=chain_config.parser.temperature,
        top_p=chain_config.parser.top_p,
    )

    return llm_parser


# Function to define prompt template
def define_prompt_template():
    pass


# Function to build LLM parser chain
def build_parse_chain():
    pass
