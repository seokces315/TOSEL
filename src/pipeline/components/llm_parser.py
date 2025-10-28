from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import JsonOutputParser


class ParsingTemplateManager:
    # Initializer
    def __init__(self, parsing_template_type):
        self.parsing_template_type = parsing_template_type

    # Template Getter
    def get_parsing_template(self):
        if self.parsing_template_type == "seokc":
            template = """
            <Role>
            You are a rule-based text-to-JSON parser.
            </Role>
            
            <Goal>
            You will be given several Outputs, and each Output may contain multiple questions.
            </Goal>
            
            <Instruction>
            Parse the provided Outputs into a JSON array.
            Each Output corresponds to one question item.
            
            JSON Structure:
            Each JSON object must strictly follow this structure:
            {{
                "materials": [] | [
                    {{
                        "content": {{
                            "text": "<string>"
                        }}
                    }},
                    ...
                ],
                "ask": None | {{
                    "text": "<string>"
                }},
                "choices": [
                    {{
                        "content": {{
                            "text": "<string>"
                        }}
                    }},
                    ...
                ]
            }}
            
            Field Rules:
            1. "materials"
                - A list of one or more objects representing the supporting text for the question.
                - "materials" include all content in the item other than the question and the choices.
                - The "materials.context.text" field should contain the complete text, preserving original line breaks as "\\n".
                - If there is no supporting text, set "materials" to an empty list ([]).
                - If multiple supporting texts are present, list each as a separate object in their original order.
                
            2. "ask"
                - An object containing the question text.
                - The "ask.text" field should contain the complete question as it appears in the source text.
                - If the original text contains a label or prefix, remove it and treat the remaining text as the question content.
                
            3. "choices"
                - A list of objects representing the answer choices in their original order.
                - If the original text contains a label of prefix, use the remaining text as the choice content.
                - Normalize any option labels to a consistent style (e.g., "(A)", "(B)", "(C)", "(D)"), adjusting automatically for the number of choices.
                
            4. If multiple questions are based on the same material, include that material content in each JSON object.
            
            5. Do NOT include any explanations, reasoning, or answers. Only reproduce the structure and text as provided.
            </Instruction>
            
            <Output Format>
            Return one JSON object per question.
            Collect all JSON objects into a single list using Python-style array brackets [ ... ].
            Do not include any text, comments, or explanation outside the list.
            Ensure each JSON object is syntactically valid and comma-separated within the array.
            </Output Format>
            
            <Output>
            {output}
            </Output>
            
            Now generate the final JSON array strictly following the above structure and rules.
            """
        else:
            template = """
                You are an assistant that formats English test data into strict JSON.

                <Instruction>
                You will be given raw test text that may contain one or more questions
                (e.g. "Question1", "Question2", etc.).

                Your job:
                - Do NOT create any new content.
                - Extract the question text, answer choices, and any supporting material from the raw text.
                - Return a JSON array in which each element is one question object.

                IMPORTANT:
                - The final response MUST be a valid JSON array: [ {{ ... }}, {{ ... }}, ... ]
                - Do NOT include any text before or after the array.
                - Use double quotes for all strings.
                - Use \\n for line breaks inside text values.
                - Remove leading labels like "A.", "B.", "C." from choices.
                - Omit any key (including top-level keys) that would be empty or unknown.
                - Do not invent difficulty, accuracy, createdUserId, tags, or isCorrect if they are not actually present.

                <Per-Question Object Shape>
                Each question should be represented (when all data exists) in this structure:

                {{
                "choices": [
                    {{
                    "content": {{
                        "type": "T",
                        "text": "a boy playing with a ball",
                        "style": {{
                        "textStyle": "string"
                        }}
                    }},
                    "index": 0,
                    "isCorrect": true
                    }}
                ],
                "materials": [
                    {{
                    "content": {{
                        "type": "T",
                        "text": "string",
                        "style": {{
                        "textStyle": "string"
                        }}
                    }},
                    "index": 0
                    }}
                ],
                "tags": [
                    {{
                    "tagCode": "string"
                    }}
                ],
                "ask": {{
                    "type": "T",
                    "text": "string",
                    "style": {{
                    "textStyle": "string"
                    }}
                }},
                "difficulty": 0,
                "accuracy": 0,
                "createdUserId": 0
                }}

                Now follow the detailed rules below for how to build each field:

                1. "ask"
                - "ask.text" is the question text.
                - Extract it from lines like "Question:", "Question1:", "What does the woman mean?", etc.
                - Include only the question prompt itself, not the answer options.
                - Always include:
                "type": "T"
                "style": {{ "textStyle": "string" }}
                - If there is no question text, omit the entire "ask" object.

                2. "choices"
                - Extract all answer choices from lines beginning with labels such as "A.", "B.", "C.", "D.", etc.
                - For each choice:
                - Remove the leading label ("A.", "B.", ...). The remaining text becomes "content.text".
                - Create an object:
                {{
                    "content": {{
                    "type": "T",
                    "text": "<choice text without the label>",
                    "style": {{
                        "textStyle": "string"
                    }}
                    }},
                    "index": <0-based index in the order they appeared>,
                    "isCorrect": true
                }}
                - Index starts at 0 and increases by 1 in display order.
                - Example:
                    A. a boy playing with a ball
                    B. a boy reading a book
                    C. a boy drawing a picture

                    becomes:
                    "choices": [
                    {{
                        "content": {{ "type": "T", "text": "a boy playing with a ball", "style": {{ "textStyle": "string" }} }},
                        "index": 0,
                        "isCorrect": true
                    }},
                    {{
                        "content": {{ "type": "T", "text": "a boy reading a book", "style": {{ "textStyle": "string" }} }},
                        "index": 1,
                        "isCorrect": true
                    }},
                    {{
                        "content": {{ "type": "T", "text": "a boy drawing a picture", "style": {{ "textStyle": "string" }} }},
                        "index": 2,
                        "isCorrect": true
                    }}
                    ]
                - If a choice label exists but the text after it is empty (e.g. "D." only), do NOT include that choice at all.
                - "isCorrect":
                - If the raw text explicitly indicates which option is correct (e.g. "Answer: B"), then:
                    - Mark that option's "isCorrect": true.
                    - For all other options in that same question:
                    - You MAY include "isCorrect": false.
                - If no correct answer information is given in the raw text:
                    - Include the choices normally, but OMIT "isCorrect" for every choice.
                - If there are no valid choices at all, omit the "choices" key entirely.

                3. "materials"
                - "materials" is for any supporting text that is needed to answer the question but is NOT itself the question sentence and NOT itself any choice.
                - Examples: passages, summaries, dialogues, instructions, descriptions of a picture, context paragraphs, etc.
                - Preserve wording exactly from the input.
                - Preserve line breaks using \\n.
                - Represent each block as:
                {{
                    "content": {{
                    "type": "T",
                    "text": "<supporting text>",
                    "style": {{
                        "textStyle": "string"
                    }}
                    }},
                    "index": <0-based index of this supporting block>
                }}
                - If multiple distinct blocks exist (for example, "Passage:" and separately "Summary:"), include them as index 0, 1, 2, ...
                - If there is no supporting material, omit "materials" entirely.

                4. "tags"
                - Only include "tags" if the raw text contains metadata that clearly maps to a tag category or code.
                - Format:
                "tags": [
                    {{ "tagCode": "<string>" }}
                ]
                - If nothing like that exists, omit "tags".

                5. "difficulty", "accuracy", "createdUserId"
                - If numbers for difficulty, accuracy, or createdUserId are explicitly provided in the raw text, include them.
                - Otherwise, omit these keys. Do NOT guess or default them to 0.

                6. Field omission rule (critical)
                - If a field would be empty, completely omit that field.
                - Examples:
                - No choices? Omit "choices".
                - No materials? Omit "materials".
                - No tags? Omit "tags".
                - No difficulty given? Omit "difficulty".
                - No correct answer given? Omit "isCorrect" from every choice object.
                - Never output empty strings "" or null just to preserve the shape.

                7. Multiple questions
                - If the raw input includes multiple questions (Question1, Question2, ...), you MUST output multiple objects.
                - Final output must be a JSON array of all question objects:
                [
                    {{ ...question 1 object... }},
                    {{ ...question 2 object... }},
                    {{ ...question 3 object... }}
                ]
                - If several questions share the same passage / context / story, you MUST repeat that same supporting text in "materials" for each question object.

                <Raw Input>
                {output}
                </Raw Input>

                Now:
                1. Extract every question.
                2. Build one JSON object per question following ALL rules above.
                3. Return a single JSON array containing those objects, and nothing else.
                """

        return template


# Function to generate LLM parser
def generate_llm_parser(chain_config):
    # Create generator object
    llm_parser = ChatOpenAI(
        openai_api_key=chain_config.parser.api_key,
        model=chain_config.parser.model_id,
        temperature=chain_config.parser.temperature,
        top_p=chain_config.parser.top_p,
    )

    return llm_parser


# Function to define prompt template
def define_parsing_prompt(parsing_template_type):
    # Define a question generation template using TemplateManager
    parsing_template_manager = ParsingTemplateManager(
        parsing_template_type=parsing_template_type
    )
    parsing_template = parsing_template_manager.get_parsing_template()

    # Create a PromptTemplate object
    parsing_prompt = PromptTemplate(
        input_variables=["output"], template=parsing_template
    )

    return parsing_prompt


# Function to build LLM parser chain
def build_parsing_chain(chain_config, parsing_template_type):
    # Get LLM parser
    llm_parser = generate_llm_parser(chain_config)
    # Get prompt template
    parsing_prompt = define_parsing_prompt(parsing_template_type)

    # Build LLM parser chain
    output_parser = JsonOutputParser()
    parser_chain = LLMChain(
        llm=llm_parser, prompt=parsing_prompt, output_parser=output_parser
    )

    return parser_chain
