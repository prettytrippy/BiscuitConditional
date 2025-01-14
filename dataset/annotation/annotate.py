import tkinter as tk
from tkinter import messagebox
import json
import numpy as np
import sys
sys.path.append("../..")
from utils import clean_text

def read_possibles(filename):
    with open(filename, "r") as file:
        # for line in file:
        #     yield line
        txt = file.read()
        txts = txt.split("\n")
    # np.random.shuffle(txts)
    for txt in txts:
        yield txt

def write_annotations(input, label, filename):
    with open(filename, "a") as file:
        json.dump({"input":input, "label":label}, file)
        # file.write(f"(\"{input}\", \"{label}\"),")
        file.write("\n")

def no_op():
    return None

class AnnotationUI:
    def __init__(self, root, string_generator):
        self.root = root
        self.string_generator = string_generator
        self.current_string = None

        # Set up the UI
        self.label = tk.Label(root, text="", font=("Arial", 16), wraplength=400)
        self.label.pack(pady=20)

        self.button_frame = tk.Frame(root)
        self.button_frame.pack()

        self.button1 = tk.Button(self.button_frame, text="Biscuit conditional", command=lambda: self.select_option(1))
        self.button1.grid(row=0, column=0, padx=10)

        self.button2 = tk.Button(self.button_frame, text="Not a biscuit conditional", command=lambda: self.select_option(0))
        self.button2.grid(row=0, column=1, padx=10)

        self.button3 = tk.Button(self.button_frame, text="Skip", command=lambda: self.next_string())
        self.button3.grid(row=0, column=2, padx=10)

        self.next_string()

    def next_string(self):
        try:
            self.current_string = next(self.string_generator)
            self.label.config(text=self.current_string)
        except StopIteration:
            messagebox.showinfo("Done", "All strings have been processed.")
            self.root.quit()

    def select_option(self, option):
        if self.current_string is not None:
            write_annotations(self.current_string, option, "annotations.jsonl")
            self.next_string()

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Annotation UI")

    strings = read_possibles("../possible_conditionals.txt")
    app = AnnotationUI(root, strings)

    root.mainloop()
