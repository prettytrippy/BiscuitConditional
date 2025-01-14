import pymupdf4llm
import re
import json

def read_jsonlines(filename):
    txt = ""
    with open(filename, 'r') as file:
        for line in file:
            json_dict = json.loads(line)
            txt += json_dict['text'] + ". "
    return txt

def read_file(filename):
    extension = filename.split(".")[-1]
    if extension == 'pdf':
        return pymupdf4llm.to_markdown(filename)
    elif extension == "jsonl":
        return read_jsonlines(filename)
    else:
        return open(filename, 'r', encoding='utf-8', errors='ignore').read()

def split_text(txt):
    sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
    sentences = sentence_endings.split(txt)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def clean_text(txt):
    cleaned_txt = re.sub(r'[^\w\s]', '', txt)
    normalized_txt = cleaned_txt.lower()
    normalized_txt = re.sub(r'\s+', ' ', normalized_txt).strip()
    return normalized_txt