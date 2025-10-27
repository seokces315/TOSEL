from .components.llm_generator import build_generator_chain
from .components.llm_parser import build_parsing_chain


# Function to build the complete LLM pipeline (Generator + Parser)
def build_complete_chain(
    chain_config, generation_template_type, prompt, example, parsing_template_type
):
    # Get LLM generator chain - 1st chain
    generator_chain = build_generator_chain(
        chain_config, generation_template_type, prompt, example
    )

    # Execute the generator chain to generate a response
    items = generator_chain.invoke({})
    items_text = items.get("text")

    return items_text

    # # Get LLM parser chain - 2nd chain
    # parser_chain = build_parsing_chain(chain_config, template_type, items_text)

    # return parser_chain
