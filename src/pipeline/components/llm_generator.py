from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


# Function to build LLM generator
def get_llm_generator(config):

    # Create generator object
    generator = ChatOpenAI(
        openai_api_key=config["GPT-4o"]["api_key"],
        model_name=config["GPT-4o"]["model_id"],
        temperature=config["GPT-4o"]["temperature"],
        top_p=config["GPT-4o"]["top_p"],
        response_format={"type": "json_object"},
    )

    return generator


# Function to define prompt template
def define_prompt_template(prompt, example):
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
