import sys
import os

from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

from ....config import config as cfg


# Function to build LLM generator
def get_llm_generator(model_id, prompt, example):

    # Create generator object
    generator = ChatOpenAI(
        openai_api_key=cfg[config]["GPT-4o"]["api_key"],
        model_name="GPT-4o",
        temperature=cfg["GPT-4o"]["temperature"],
        top_p=cfg["GPT-4o"]["top_p"],
        response_format={"type": "json_object"},
    )
    print("get llm generator")
    return generator


# Function to define prompt template
def define_prompt_template(model_id):
    """
    TODO
    prompt, example 인자 전달받아 PromptTemplate 생성

    template = f/"/"/"
    프롬프트 엔지니어링
    /"/"/"

    prompt_template = PromptTemplate(input_variables=[], template=template)
    return -> prompt_template
    """


# Function to build LLM generator
def build_1st_chain(generator, prompt_template):
    pass
