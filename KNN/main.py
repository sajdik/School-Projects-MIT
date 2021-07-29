import pandas
import numpy as np

import torch
import torch.nn as nn
from dataset import Data
from model import NCF
from evaluate import evaluate


device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

def main():
    np.random.seed(123)
    print("Loading data...")
    data = Data('dataset/dataset.csv', 'dataset/games.csv', 0.01)
    print("Creating model...")
    model = NCF(data.num_users, data.num_items, data.publisherCount, data.featureCount)
    model = model.to(device)

    print("Training...")
    model.train(data, 5)
    print("Evaluating...")
    hit, ndcg = evaluate(model, data)
    print("Hit Ratio @ 10 is {:.2f}".format(hit))
    print("NDCG @ 10 is {:.2f}".format(ndcg))


if __name__ == "__main__":
    main()