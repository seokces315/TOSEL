import sys
import os

from langchain import LLMChain
from langchain import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI

from config import config as cfg


# Function to build LLM generator
def get_llm_generator(model_id):
    print("get llm generator --")

    # Create generator object
    llm = ChatOpenAI(
        openai_api_key=cfg[model_id]["generator"]["api_key"],
        model_name="gpt-4o",
        temperature=cfg[model_id]["generator"]["temperature"],
        top_p=cfg[model_id]["generator"]["top_p"],
    )

    return llm


# # Function to define prompt template
# def get_prompt_template(prompt, example):

#     template = f"""
#     You are a highly skilled English test generation assistant.

#     <Main Task>
#     {prompt}
#     </Main Task>

#     <Reference Example>
#     The following example shows the general format and structure of questions.
#     Use it ONLY as a stylistic and structural reference.
#     Do NOT copy or paraphrase the content. Follow the <Main Task> instructions strictly.

#     {example}
#     </Reference Example>

#     <Output Requirements>
#     - Follow ALL details and constraints described in <Main Task>.
#     - Use the example ONLY to mirror the format (dialogue → question → 4 options).
#     - Ensure that the generated question aligns with the task definition and difficulty level.
#     - Maintain consistency in tone, grammar, and structure across all question sets.
#     </Output Requirements>

#     Generate the output below:
#     Question:
#     Options:
#     """

#     prompt_template = PromptTemplate(input_variables=[], template=template)
#     return prompt_template


def get_prompt_template(prompt, example):
    template = f"""
    You are a highly skilled English test generation assistant.

    <Instruction>
    {prompt}
    Follow these instruction
    </Instruction>

    <Example>
    Here is some example.
    Do NOT copy or paraphrase its wording or specific content.
    {example}
    </Example>

    Based on the shape of Example question above, Generate Question and Options.
    Question:
    Options:

    # 여기서부터 parser template이니까 그대로 복붙해봐
    Return one valid json object only (no prose, no markdown, no code fences) using this schema:

    {{
    "ask": {{
        "1": "question text",
        "2": "question text"
    }},
    "material": {{
        "passage": {{
        "1": "passage text or empty if none",
        "2": "passage text or empty if none"
        }},
        "options": {{
        "1": {{"A":"option text","B":"option text","C":"option text","D":"option text"}},
        "2": {{"A":"option text","B":"option text","C":"option text","D":"option text"}}
        }}
    }}
    }}

    Normalization rules:
    - Only put question sentences into ask["n"] (remove labels like "Q1", "Question1", etc.)
    - Put passage into material["passage"]["n"] (use "" if none)
    - Put options for each question into material["options"]["n"] using labels "A", "B", "C", "D", ... according to the number of options.
    - Output must be valid JSON
    """

    return PromptTemplate(input_variables=[], template=template)


# Function to build LLM generator
def generating_chain(model_id, prompt, example):

    llm = get_llm_generator(model_id)
    template = get_prompt_template(prompt, example)

    llm_generator = LLMChain(prompt=template, llm=llm)

    return llm_generator
