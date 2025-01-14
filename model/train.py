import json
import numpy as np
import torch
import torch.nn as nn
from classifier import TextClassificationModel
import matplotlib.pyplot as plt

batch_size = 50

def make_training_set():
    rets = []
    chunk = []
    count = 0

    with open("../dataset/annotation/annotations.jsonl", 'r') as file:
        lines = file.read().split("\n")

    lines = [line for line in lines if line]
    np.random.shuffle(lines)
    
    for line in lines:
        if count == batch_size:
            rets.append(chunk)
            chunk = []
            count = 0

        try:
            json_dict = json.loads(line)
        except:
            print("LINE:", line)
        chunk.append((json_dict['input'], torch.tensor(float(json_dict['label']))))
        count += 1

    rets.append(chunk)
    return rets

def train_model(model, train_loader, epochs):
    loss_fn = nn.BCELoss()
    optimizer = torch.optim.AdamW(model.parameters(), lr=1e-5)

    for epoch in range(epochs):
        model.train()
        train_loss = 0

        for (input, label) in train_loader[epoch]:
            optimizer.zero_grad()

            outputs = model(input)
            loss = loss_fn(outputs.squeeze(), label)

            loss.backward()
            optimizer.step()

            train_loss += loss.item()
        
        print(f"[Epoch {epoch+1}/{epochs}] Loss: {train_loss/len(train_loader[epoch])}")

if __name__ == "__main__":
    model = TextClassificationModel()
    model.load_state_dict(torch.load("model_weights.pth"))

    dataset = make_training_set()
    trainloader = dataset[:-1]
    testloader = dataset[-1]
    train_model(model, trainloader, epochs=len(trainloader))

    # Eval
    trues = []
    guesses = []

    model.eval()
    with torch.no_grad():
        model.eval()
        for (txt, label) in testloader:
            observed = model(txt).item()
            label = label.item()
            trues.append(label)
            guesses.append(observed)

        torch.save(model.state_dict(), 'model_weights.pth')

        guesses = np.array(guesses)
        guesses /= np.max(guesses)

        plt.plot(trues)
        plt.plot(guesses)
        plt.show()

        print(model("There's biscuits on the table, if you want some.").item())
        print(model("If he is a dog, he is a mammal.").item())