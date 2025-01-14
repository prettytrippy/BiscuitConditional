import sys
sys.path.append("..")
from annotate import write_annotations, read_possibles
import numpy as np
from tqdm import tqdm
from contrived_examples import contrived_examples
from akashic.utils import count_tokens
from akashic.agents.chatbot import AkashicChatbot
from akashic.model import AkashicModel

model = AkashicModel("Llama-3.2-3B-Instruct-Q6_K.gguf", context_length=4096)
chatter = AkashicChatbot(model, system_message="")

prompt_preamble = """
Your job is to label conditional statements as either biscuit conditionals or not.
A biscuit conditional is a conditional where the conclusion is true regardless of the premise.

For example:

"There are biscuits on the table if you want some."
This is a biscuit conditional because the conclusion ("There are biscuits on the table") is true regardless of the premise ("if you want some").
Key points to remember:
All the examples given will contain an "if" statement premise, but not necessarily a conclusion.
A biscuit conditional must have a clear premise and conclusion. 
Never label a conditional as a biscuit conditional if it does not have a conclusion.
Don't even guess at a conclusion if one is implied, just assume it is not a biscuit conditional.
Never label a sentence as a biscuit conditional if the conclusion might be false, or might depend on the premise.
Only declarations can be biscuit conditionals, never commands or questions.

Given a conditional string, return answers in this format:
{{"input":"<conditional string>", "label":<0 (not a biscuit conditonal) or 1 (biscuit conditonal)>}}
"""

def process_prompt(txt):
    return f"{prompt_preamble}\nHere's the conditional to classify:\n{txt}"

def wrap_example(example):
    txt, label = example
    return [{"role":"user", "content":process_prompt(txt)}, {"role":"assistant", "content":label}]

messages = []

for example in contrived_examples:
    messages.extend(wrap_example(example))

possibles = read_possibles("../../possible_conditionals.txt")

num_retries = 3

for possible in tqdm(possibles, desc="Labelling"):
    response = ""

    for i in range(num_retries):
        if response != "0" and response != "1":
            chatter.messages = messages
            response = list(chatter.send_prompt(process_prompt(possible), stream=False))[0]
            # print(possible, response)
        else:
            break

    if response == "0" or response == "1": 
        write_annotations(possible, int(response), "../annotations.jsonl")

