from components.llm_generator import get_llm_generator
from components.llm_parser import parsing_llm


def chain_run(model_id, prompt, example):
    generator = get_llm_generator(model_id)
    parser = parsing_llm(model_id)

    output1 = generator.predict()
    output2 = parser.run(output1)
    return output1, output2
