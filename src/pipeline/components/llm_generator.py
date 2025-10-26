from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


# Manage multiple prompt templates for item generation
class GenerationTemplateManager:
    # Initializer
    def __init__(self, template_type):
        self.template_type = template_type

    # Template Getter
    def get_generation_template(self, prompt, example):
        if self.template_type == "xml":
            template = f"""
            You are an expert English test item writer.

            <Guideline>
            {prompt}
            </Guideline>

            <Example>
            Use the following examples only as a reference for structure and format.
            Do not copy or adapt their wording or ideas.
            {example}
            </Example>

            Write plain text without any headings, categories, or special symbols.
            Keep only the necessary passage/question and answer option labels.
            Generate new items following the Example's structure, including Passage/Question and Options.
            """
        else:
            template = f"""
            You are an expert English test item writer.

            [Guideline]
            {prompt}
            [/Guideline]

            [Example]
            Use the following examples only as a reference for structure and format.
            Do not copy or adapt their wording or ideas.
            {example}
            [/Example]

            Write plain text without any headings, categories, or special symbols.
            Keep only the necessary passage/question and answer option labels.
            Generate new items following the Example's structure, including Passage/Question and Options.
            """

        return template


# Function to generate LLM generator
def generate_llm_generator(chain_config):
    # Create generator object
    llm_generator = ChatOpenAI(
        openai_api_key=chain_config.generator.api_key,
        model=chain_config.generator.model_id,
        temperature=chain_config.generator.temperature,
        top_p=chain_config.generator.top_p,
    )

    return llm_generator


# Function to define prompt template
def define_prompt_template(template_type, prompt, example):
    # Define a question generation template using TemplateManager
    template_manager = GenerationTemplateManager(template_type=template_type)
    template = template_manager.get_generation_template(prompt=prompt, example=example)

    # Create a PromptTemplate object
    prompt_template = PromptTemplate(input_variables=[], template=template)

    return prompt_template


# Function to build LLM generator chain
def build_generator_chain(chain_config, template_type, prompt, example):
    # Get LLM generator
    llm_generator = generate_llm_generator(chain_config)
    # Get prompt template
    prompt_template = define_prompt_template(template_type, prompt, example)

    # Build LLM generator chain
    generator_chain = LLMChain(llm=llm_generator, prompt=prompt_template)

    return generator_chain
