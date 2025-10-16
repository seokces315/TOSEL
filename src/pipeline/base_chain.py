# from components.llm_generator import get_llm_generator
from pipeline.components.llm_parser import parsing_llm
from pipeline.components.llm_generator import get_llm_generator


def chain_run(model_id, prompt, example):
    llm_generator = generating_chain(model_id, prompt, example)  # LLM chain
    # parser = parsing_llm(model_id)  # parser chain

    output1 = llm_generator.predict()
    # output2 = parser.run(output1)

    # return output1, output2
    print("output1", output1)
    return output1
