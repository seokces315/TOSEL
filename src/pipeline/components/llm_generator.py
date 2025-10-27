from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


# Manage multiple prompt templates for item generation
class GenerationTemplateManager:
    # Initializer
    def __init__(self, generation_template_type):
        self.generation_template_type = generation_template_type

    # Template Getter
    def get_generation_template(self, prompt, example):
        if self.generation_template_type == "xml":
            template = f"""
            <Role>
            You are an expert English test item writer.
            </Role>

            <Guideline>
            {prompt}
            </Guideline>

            <Example>
            Use the following examples only as a reference for structure and format.
            Do not copy or adapt their wording or ideas.
            {example}
            </Example>

            <Output Format>
            Write plain text without any headings, categories, or special symbols.
            Keep only the necessary passage/question and answer option labels.
            Generate new items following the Example's structure, including Passage/Question and Options.
            </Output Format>
            """
        else:
            template = f"""
            [Role]
            You are an expert English test item writer.
            [/Role]

            [Guideline]
            {prompt}
            [/Guideline]

            [Example]
            Use the following examples only as a reference for structure and format.
            Do not copy or adapt their wording or ideas.
            {example}
            [/Example]

            [Output Format]
            Write plain text without any headings, categories, or special symbols.
            Keep only the necessary passage/question and answer option labels.
            Generate new items following the Example's structure, including Passage/Question and Options.
            [/Output Format]            
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
def define_generation_prompt(generation_template_type, prompt, example):
    # Define a question generation template using TemplateManager
    template_manager = GenerationTemplateManager(
        generation_template_type=generation_template_type
    )
    generation_template = template_manager.get_generation_template(
        prompt=prompt, example=example
    )

    # Create a PromptTemplate object
    generation_prompt = PromptTemplate(input_variables=[], template=generation_template)

    return generation_prompt


# Function to build LLM generator chain
def build_generator_chain(chain_config, generation_template_type, prompt, example):
    # Get LLM generator
    llm_generator = generate_llm_generator(chain_config)
    # Get prompt template
    generation_prompt = define_generation_prompt(
        generation_template_type, prompt, example
    )

    # Build LLM generator chain
    generator_chain = LLMChain(llm=llm_generator, prompt=generation_prompt)

    return generator_chain
