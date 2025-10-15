# Load and return the example data from the given file path
def load_example(example_path):

    # Load the specified example file
    with open(example_path, "r", encoding="utf-8") as f:
        example = f.read()

    return example
