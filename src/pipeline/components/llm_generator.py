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

    if not passage:
        template = f"""
        You are a highly skilled English test generation assistant.

        <Main Task>
        {prompt_content}
        </Main Task>

        <Reference Example>
        The following example shows the general format and structure of questions.
        Use it ONLY as a stylistic and structural reference.
        Do NOT copy or paraphrase the content. Follow the <Main Task> instructions strictly.
        
        {example_content}
        </Reference Example>

        <Output Requirements>
        - Follow ALL details and constraints described in <Main Task>.
        - Use the example ONLY to mirror the format (dialogue → question → 4 options).
        - Ensure that the generated question aligns with the task definition and difficulty level.
        - Maintain consistency in tone, grammar, and structure across all question sets.
        </Output Requirements>

        Generate the output below:
        Question:
        Options:
        """
    else:
        template = f"""
        You are a highly skilled English test generation assistant.

        <Main Task>
        {prompt_content}
        </Main Task>

        <Reference Example>
        The following example shows the format and structure of questions using a given passage.
        Use it ONLY as a structural guide.
        Do NOT modify or recreate the passage. Follow the <Main Task> strictly.
        
        {example_content}
        </Reference Example>

        <Output Requirements>
        - Use the given passage exactly as it is. Do NOT create a new passage.
        - Follow all requirements and constraints from <Main Task>.
        - Use the example for format only.
        - Ensure the level, structure, and language meet advanced EFL standards.
        </Output Requirements>

        Generate the output below:
        Question:
        Options:
        """

    prompt = PromptTemplate(input_variables=[], template=template)
    return template


# Function to build LLM generator
def generating_chain(model_id, prompt, example):

    llm = get_llm_generator(model_id)
    template = get_prompt_template(prompt, example)

    llm_generator = LLMChain(prompt=template, llm=llm)

    return llm_generator
