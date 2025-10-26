from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain.chains import LLMChain

from langchain_core.output_parsers import JsonOutputParser


class ParsingTemplateManager:
    # Initializer
    def __init__(self, parsing_type):
        self.parsing_type = parsing_type

    # Template Getter
    def get_parsing_template(self):
        if self.parsing_type == "seokc":
            template = """
            You are a rule-based text-to-JSON parser.
            You will be given several Outputs, and each Output may contain multiple questions.
            
            <Instruction>
            Parse the provided Outputs into a JSON array.
            Each Output corresponds to one question item.
            
            Output Format:
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
                - If the original text contains a label or prefix, remove it and keep only the question text.
                
            3. "choices"

            Field rules:
            2. "choice.options"
                - A list of four answer choices in order.
                - You MUST preserve the labels (A., B., C., D.) if they exist.
                - If the source uses A1/B1 or A2/B2 style, normalize them to "A.", "B.", "C.", "D." in the output.

            4. If multiple questions (Question1, Question2, ...) share the same material (same Passage / Summary / Dialogue), include that same material content again in each JSON object.

            5. Do NOT add any explanations, reasoning steps, or answers. Only structure and text from the provided example.
            
            Important:
            - Return one JSON object per question.
            - Output all JSON objects in a Python-style list [ ... ].
            - Do not include any text or explanation outside the list.
            - Ensure each JSON object is syntactically valid and comma-separated within the list.
            
            </Instruction>
            """
        else:
            template = """
            You are a helpful English test generator.

            <Instruction>
            You will be given an Instruction (what kind of question to generate) and an Example (sample input format).
            Your job is to analyze the Example and produce test items in JSON.

            Important:
            - A single Example may actually contain multiple questions (Question1, Question2, ...).
            - You MUST return one JSON object per question.
            - Output all JSON objects in a Python-style list [ ... ] with commas between them.
            - Do NOT include any text outside the list.

            <JSON Schema>
            Each JSON object must follow this structure exactly:

            {{
                "ask": {{
                    "question": "<string>"
                }},
                "choice": {{
                    "options": [
                        "A. <option text>",
                        "B. <option text>",
                        "C. <option text>",
                        "D. <option text>",
                    ]
                }},
                "material": {{
                    "content": "<string>"
                }}
            }}

            Field rules:
            1. "ask.question"
                - The actual question text (ex: "Choose the most suitable word for blank [A].").
                - If the original data uses "Question:" or "Question1:", use that question text.

            2. "choice.options"
                - A list of four answer choices in order.
                - You MUST preserve the labels (A., B., C., D.) if they exist.
                - If the source uses A1/B1 or A2/B2 style, normalize them to "A.", "B.", "C.", "D." in the output.

            3. "material.content"
                - Everything that is NOT the question text or the options, but is needed to solve the question.
                - This can include any/all supporting info such as:
                    - Passage
                    - Summary
                    - Dialogue
                    - Descriptions
                    - Context setup before "Question:"
                - Keep line breaks using "\\n".
                - If there is no extra supporting text, set "content" to "" (empty string).

            4. If multiple questions (Question1, Question2, ...) share the same material (same Passage / Summary / Dialogue), include that same material content again in each JSON object.

            5. Do NOT add any explanations, reasoning steps, or answers. Only structure and text from the provided example.

            <Output Format Rules>
            - Your final response MUST be a single JSON array (list) of one or more question objects.
            - Do NOT wrap the array in any additional keys.
            - Do NOT include comments or prose outside the array.
            - The output must be valid JSON (double quotes, proper commas, etc.).

            </Instruction>

            <Output>
            {output}
            </Output>

            Now generate the output JSON array based on the Example.
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
def define_prompt_template(parsing_type):
    # Define a question generation template using TemplateManager
    template_manager = ParsingTemplateManager(parsing_type=parsing_type)
    template = template_manager.get_parsing_template()

    # Create a PromptTemplate object
    prompt_template = PromptTemplate(input_variables=["output"], template=template)
    print(prompt_template.input_variables)

    return prompt_template


# Function to build LLM parser chain
def build_parsing_chain(chain_config, parsing_type, output):
    # Get LLM parser
    llm_parser = generate_llm_parser(chain_config)
    # Get prompt template
    prompt_template = define_prompt_template(parsing_type)

    # Build LLM parser chain
    parser = JsonOutputParser()
    parser_chain = LLMChain(
        llm=llm_parser, prompt=prompt_template, output_parser=parser
    )
    result = parser_chain.run(output)

    return result
