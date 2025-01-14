import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoModel
import matplotlib.pyplot as plt

class TextClassificationModel(nn.Module):
    def __init__(self, transformer_name="distilbert-base-uncased", dropout=0.3):
        super(TextClassificationModel, self).__init__()
        
        self.tokenizer = AutoTokenizer.from_pretrained(transformer_name)
        self.transformer = AutoModel.from_pretrained(transformer_name)
        
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(self.transformer.config.hidden_size, 1)
        self.sigmoid = nn.Sigmoid()
        self.relu = nn.ReLU()

    def forward(self, text):
        # with torch.no_grad():
        encoding = self.tokenizer(text, 
                                padding=True, 
                                truncation=True, 
                                return_tensors="pt")
        
        input_ids = encoding['input_ids']
        attention_mask = encoding['attention_mask']
        
        transformer_output = self.transformer(input_ids, attention_mask=attention_mask)
        
        cls_output = transformer_output.last_hidden_state[:, 0, :]
    
        x = cls_output
        
        x = self.fc(x)
        # thingy = self.fc.state_dict()['weight'].detach().numpy().squeeze()
        # print(thingy.shape)
        # plt.plot(thingy)
        # plt.show()
        x = self.sigmoid(x)
        return x