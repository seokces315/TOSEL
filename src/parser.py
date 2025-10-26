import argparse


# Args parser
def parse_args():
    # Define parser
    parser = argparse.ArgumentParser(description="TOSEL question generation settings")

    parser.add_argument("--comprehension_type", default="LC", type=str)
    parser.add_argument("--problem_type", default="A", type=str)
    parser.add_argument("--level", default="ADV", type=str, help="Difficulty level")

    parser.add_argument("--model_id", default="gpt-4o", type=str, help="Model type")
    parser.add_argument("--template_type", default="xml", type=str)
    parser.add_argument("--parsing_type", default="sohee", type=str, help="Test")

    args = parser.parse_args()

    return args
