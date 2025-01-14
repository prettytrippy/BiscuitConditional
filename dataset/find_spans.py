import sys
from glob import glob
from tqdm import tqdm
sys.path.append("..")
from utils import *

def contains_if(txt):
    txt = clean_text(txt).lower()
    return " if " in txt

def get_spans(regex):
    files = glob(regex)
    results = []
    for file in tqdm(files, "Processing files"):
        txt = read_file(file)
        sentences = split_text(txt)
        sentences = [sentence for sentence in sentences if contains_if(sentence)]
        results.extend(sentences)
    return results

def store_results(filename, results):
    with open(filename, "a") as file:
        for result in tqdm(results, desc="Storing results"):
            file.write(result[:-1]+"\n")

def pipeline(regex, filename):
    results = get_spans(regex)
    store_results(filename, results)
    
if __name__ == "__main__":
    pipeline("movie-corpus/utterances.jsonl", "possible_conditionals.txt")