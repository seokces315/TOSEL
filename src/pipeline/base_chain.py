from components.llm_generator import build_generator_chain


# Function to build the complete LLM pipeline (Generator + Parser)
def build_complete_chain(chain_config, prompt, example):

    # Get LLM generator chain - 1st chain
    generator_chain = build_generator_chain(chain_config, prompt, example)

    # Get LLM parser chain - 2nd chain
