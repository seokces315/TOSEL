from parser import parse_args
from loaders.prompt_loader import load_prompt
from loaders.example_loader import load_example
from loaders.config_loader import load_config

from pipeline.base_chain import chain_run


def main(args):
    # Initialize variables from input arguments
    model_id = args.model_id
    comprehension_type = args.comprehension_type
    problem_type = args.problem_type
    level = args.level

    # Load prompt & example
    prompt_path = (
        f"../bank/prompt/{comprehension_type}_{problem_type}_{level}_prompt.txt"
    )
    example_path = (
        f"../bank/example/{comprehension_type}_{problem_type}_{level}_example.txt"
    )
    prompt = load_prompt(prompt_path=prompt_path)
    example = load_example(example_path=example_path)

    # Run pipeline
    print(f"start chain run --")
    print(f"model_id: {model_id}")
    chain_run(model_id, prompt, example)
    # 1. llm_generator
    # 2. llm_parser(return type : Json)


if __name__ == "__main__":
    args = parse_args()
    main(args)
