from parser import parse_args

from loaders.prompt_loader import load_prompt
from loaders.example_loader import load_example

from utils.config import ChainConfig, GeneratorConfig, ParserConfig

from pipeline.base_chain import build_complete_chain

import warnings

warnings.filterwarnings(action="ignore")

import time


def main(args):
    # Measure execution time
    start_time = time.time()

    # Load prompt & example
    comprehension_type = args.comprehension_type
    problem_type = args.problem_type
    level = args.level
    prompt_path = (
        f"../bank/prompt/{comprehension_type}_{problem_type}_{level}_prompt.txt"
    )
    example_path = (
        f"../bank/example/{comprehension_type}_{problem_type}_{level}_example.txt"
    )
    prompt = load_prompt(prompt_path=prompt_path)
    example = load_example(example_path=example_path)

    # Initialize LLM chain pipeline
    model_id = args.model_id
    template_type = args.template_type
    chain_config = ChainConfig(
        generator=GeneratorConfig(model_id=model_id),
        parser=ParserConfig(model_id=model_id),
    )
    complete_chain = build_complete_chain(chain_config, template_type, prompt, example)

    # Execute the chain to generate a response
    result = complete_chain.invoke({})
    print(result.get("text"))

    # Print execution time
    end_time = time.time()
    elapsed = end_time - start_time
    print(f"\nElapsed time: {elapsed:.2f}초")


if __name__ == "__main__":
    args = parse_args()
    main(args)
