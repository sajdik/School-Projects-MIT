import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split
from dataset import Data
from evaluate import evaluate


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

class NCF(nn.Module):
    
    # Model initialization
    def __init__(self, userCount, itemCount, publisherCount, featureCount):
        super(NCF, self).__init__()
        self.user_embedding = nn.Embedding(num_embeddings=userCount, embedding_dim=8)
        self.item_embedding = nn.Embedding(num_embeddings=itemCount, embedding_dim=8)
        self.publisher_embeding = nn.Embedding(num_embeddings=publisherCount, embedding_dim=8)
        inputSize = 3*8 + featureCount + 1                                  # 3*8 za embeddingy, 1 za cenu a featureCount je pocet zanru a specifikaci

        # Neural Net architecture - 87x64x32x1
        self.fc0 = nn.Linear(in_features=inputSize, out_features=64)
        self.fc1 = nn.Linear(in_features=64, out_features=32)
        self.output = nn.Linear(in_features=32, out_features=1)

    def forward(self, user_input, item_input, publisher_input, price, features):
        user_embedded = self.user_embedding(user_input)
        item_embedded = self.item_embedding(item_input)
        publisher_embedded = self.publisher_embeding(publisher_input)

        price = torch.unsqueeze(price, 1)
        vector = torch.cat([user_embedded, item_embedded, publisher_embedded, price, features], dim=-1)

        vector = nn.ReLU()(self.fc0(vector))
        vector = nn.ReLU()(self.fc1(vector))
        pred = nn.Sigmoid()(self.output(vector))

        return pred

    def train(self, data, epochs_num = 5, learning_rate=1e-3):
        optimizer = torch.optim.Adam(self.parameters(), lr=learning_rate)

        for _ in range (epochs_num):
            for train_batch in data.train_dataLoader:
                # Load batch
                user_id, item_id, label = train_batch
                publisher_id = torch.tensor([data.get_publisher(item) for item in item_id])
                prices = torch.tensor([data.get_price(item) for item in item_id], dtype=torch.float32)
                features = torch.tensor([data.get_features(item) for item in item_id], dtype=torch.float32)

                # GPU handling
                features = features.to(device)
                label = label.to(device)
                user_id = user_id.to(device)
                item_id = item_id.to(device)
                publisher_id = publisher_id.to(device)
                prices = prices.to(device)

                # Forward + back propagation
                logits = self.forward(user_id, item_id, publisher_id, prices, features)
                loss = nn.BCELoss()(logits, label.view(-1, 1).float())
                loss.backward()
                optimizer.step()
                optimizer.zero_grad()
            
            # Validation after each epoch 
            with torch.no_grad():
                val_loss = []
                for val_batch in data.val_dataLoader:
                    user_id, item_id, label = val_batch
                    publisher_id = torch.tensor([data.get_publisher(item) for item in item_id])
                    prices = torch.tensor([data.get_price(item) for item in item_id], dtype=torch.float32)
                    features = torch.tensor([data.get_features(item) for item in item_id], dtype=torch.float32)

                    features = features.to(device)
                    label = label.to(device)
                    user_id = user_id.to(device)
                    item_id = item_id.to(device)
                    publisher_id = publisher_id.to(device)
                    prices = prices.to(device)
                    logits = self.forward(user_id, item_id, publisher_id, prices,features)
                    val_loss.append(nn.BCELoss()(logits, label.view(-1, 1).float()).item()) #TODO

                val_loss = torch.mean(torch.tensor(val_loss))
                print('val_loss: ', val_loss.item())
            