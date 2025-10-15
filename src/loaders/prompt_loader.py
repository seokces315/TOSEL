# Load and return the prompt template from the given file path
def load_prompt(prompt_path):

    # Load the specified prompt file
    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt = f.read()

    return prompt
