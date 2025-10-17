from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain


# Function to generate LLM generator
def generate_llm_generator(chain_config):
    # Create generator object
    generator = ChatOpenAI(
        openai_api_key=chain_config.generator.api_key,
        model=chain_config.generator.model_id,
        temperature=chain_config.generator.temperature,
        top_p=chain_config.generator.top_p,
    )

    return generator


# Function to define prompt template
def define_prompt_template(prompt, example):
    # Design a template for generating questions
    template = f"""
    You are a helpful English test assistant.
    <Instruction>
    {prompt}
    </Instruction>
        
    <Example>
    Here is some example.
    {example}
    </Example>
        
    Based on the shape of Example question above, Generate Question and Options.
    Question:
    Options:
    """

    # Create a PromptTemplate object
    prompt_template = PromptTemplate(input_variables=[], template=template)

    return prompt_template


# Function to build LLM generator chain
def build_generator_chain(chain_config, prompt, example):
    # Get LLM generator
    generator = generate_llm_generator(chain_config)
    # Get prompt template
    prompt_template = define_prompt_template(prompt, example)

    # Build LLM generator chain
    generator_chain = LLMChain(llm=generator, prompt=prompt_template)

    return generator_chain
