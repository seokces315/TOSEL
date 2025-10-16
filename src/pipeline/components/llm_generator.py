import sys
import os

from langchain import LLMChain
from langchain import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from config import config as cfg


# Function to build LLM generator
def get_llm_generator(model_id):

    # Create generator object
    llm = ChatOpenAI(
        openai_api_key=cfg[model_id]["generator"]["api_key"],
        model_name="GPT-4o",
        temperature=cfg[model_id]["generator"]["temperature"],
        top_p=cfg[model_id]["generator"]["top_p"],
        response_format={"type": "json_object"},
    )

    return llm


# Function to define prompt template
def get_prompt_template(prompt, example):
    """
    TODO
    prompt, example 인자 전달받아 PromptTemplate 생성

    template = f/"/"/"
    프롬프트 엔지니어링
    /"/"/"

    prompt_template = PromptTemplate(input_variables=[], template=template)
    return -> prompt_template
    """

    prompt = PromptTemplate(input_variables=[], template=template)
    return template


# Function to build LLM generator
def generating_chain(model_id, prompt, example):

    llm = get_llm_generator(model_id)
    template = get_prompt_template(prompt, example)

    llm_generator = LLMChain(prompt=template, llm=llm)

    return llm_generator
