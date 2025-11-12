from .components.llm_generator import build_generator_chain
from .components.llm_parser import build_parsing_chain

from .schema import Content, Material, Ask, Choice, Item


# Function to build the complete LLM pipeline (Generator + Parser)
def build_complete_chain(
    chain_config,
    generation_template_type,
    prompt,
    example,
    parsing_template_type,
):
    # Get LLM generator chain - 1st chain
    generator_chain = build_generator_chain(
        chain_config, generation_template_type, prompt, example
    )

    # Execute the generator chain to generate a response
    items = generator_chain.invoke({})
    items_text = items.get("text")
    print("items_text", items_text)

    # Get LLM parser chain - 2nd chain
    parser_chain = build_parsing_chain(chain_config, parsing_template_type)

    return items_text, parser_chain


# Function to dynamically build a list of objects based on the provied schema definition
def build_objects_from_schema(result):
    # Create a list to store item objects
    item_list = list()

    # For loop
    for res in result:
        materials = []
        ask = None

        # Generate materials
        if res.get("materials"):
            materials = [
                Material(content=Content(text=mat["content"]["text"]), index=j)
                for j, mat in enumerate(res["materials"])
            ]

        # Generate ask
        if res.get("ask"):
            ask = Ask(text=res["ask"]["text"])

        # Generate choices
        choices = [
            Choice(
                content=Content(text=choice["content"]["text"]),
                index=j,
                isCorrect=(j == 0),
            )
            for j, choice in enumerate(res["choices"])
        ]

        # Build Item
        item = Item(materials=materials, ask=ask, choices=choices)

        # Append the item to the list
        item_list.append(item)

    return item_list
