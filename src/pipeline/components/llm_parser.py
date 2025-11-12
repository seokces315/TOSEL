from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser


class ParsingTemplateManager:
    # Initializer
    def __init__(self, parsing_template_type):
        self.parsing_template_type = parsing_template_type

    # Template Getter
    def get_parsing_template(self):
        template = """
            You are an assistant that converts raw English test text into a valid JSON array.

            Schema per question:
            [
            {{
                "ask": {{ "text": "string" }},
                "choices": [ {{ "text": "string" }}, {{ "text": "string" }}, ... ],
                "materials": [ {{ "text": "string" }}, {{ "text": "string" }}, ... ]
            }}
            ]

            Rules:
            - Output ONLY a valid JSON array (no extra text).
            - Do NOT invent/modify content.
            - Use double quotes; use \\n for line breaks.
            - Omit any key if its content is missing or empty.
            - Multiple questions → multiple objects.
            - Mapping:
            * ask.text  ← question text (from "Question:", etc.)
            * choices[].text ← options (A./B./C./D., remove labels)
            * materials[].text ← remaining context (dialogue, passage, summary, etc.)

            <Raw Input>
            {output}
            </Raw Input>

            Return ONLY the final JSON array.
        """
        return template


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
def define_parsing_prompt(parsing_template_type):
    # Define a question generation template using TemplateManager
    parsing_template_manager = ParsingTemplateManager(
        parsing_template_type=parsing_template_type
    )
    parsing_template = parsing_template_manager.get_parsing_template()

    # Create a PromptTemplate object
    parsing_prompt = PromptTemplate(
        input_variables=["output"], template=parsing_template
    )

    return parsing_prompt


# Function to build LLM parser chain
def build_parsing_chain(chain_config, parsing_template_type):
    # Get LLM parser
    llm_parser = generate_llm_parser(chain_config)
    # Get prompt template
    parsing_prompt = define_parsing_prompt(parsing_template_type)

    # Build LLM parser chain
    output_parser = JsonOutputParser()
    parser_chain = LLMChain(
        llm=llm_parser, prompt=parsing_prompt, output_parser=output_parser
    )

    return parser_chain
