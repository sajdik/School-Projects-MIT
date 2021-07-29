import pandas
import numpy as np

import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader, random_split

# Util class for dataset creation
class SteamDataset(Dataset):
    def __init__(self, matrix, all_gameIds):
        self.users, self.items, self.labels = self.get_dataset(matrix, all_gameIds)

    def __len__(self):
        return len(self.users)
  
    def __getitem__(self, idx):
        return self.users[idx], self.items[idx], self.labels[idx]

    def get_dataset(self, matrix, all_gameIds):
        users, items, labels = [], [], []
        user_item_set = set(zip(matrix['user_id'], matrix['game_id']))

        num_negatives = 4
        # Adding num_negatives negative samples for each positive 
        for u, i in user_item_set:
            users.append(u) 
            items.append(i)
            labels.append(1)
            for _ in range(num_negatives):
                negative_item = np.random.choice(all_gameIds)
                while (u, negative_item) in user_item_set:
                    negative_item = np.random.choice(all_gameIds)
                users.append(u)
                items.append(negative_item)
                labels.append(0)

        return torch.tensor(users), torch.tensor(items), torch.tensor(labels)


class Data:
    def __init__(self, dataset_path, games_data_path, cut=1):
        # Read matrices from .csv files
        matrix = pandas.read_csv(dataset_path)
        self.games = pandas.read_csv(games_data_path)
        self.publisherCount = self.games["publisher"].max() + 1
        self.featureCount = self.games.drop(['game_id', 'publisher', 'price'],axis=1).shape[1]

        # Get cut from samples
        rand_userIds = np.random.choice(matrix['user_id'].unique(), 
                                        size=int(len(matrix['user_id'].unique())*cut), 
                                        replace=False)
        matrix = matrix.loc[matrix['user_id'].isin(rand_userIds)]

        # Test dataset - one record from each user
        test_data = matrix.groupby("user_id").sample(n=1, random_state=1)
        self.test_user_item_set = set(zip(test_data['user_id'], test_data['game_id']))

        # Removing test saples from original dataset
        data = pandas.concat([matrix, test_data, test_data]).drop_duplicates(keep=False)
        data['bought'] = 1

        self.all_gameIds = matrix['game_id'].unique()

        # Spliting data to train and validation
        mask = np.random.rand(len(data)) < 0.9  
        train_dataLoader = data[mask]
        val_dataLoader = data[~mask]

        # Creating data loaders for batching
        self.train_dataLoader = DataLoader(SteamDataset(train_dataLoader, self.all_gameIds),batch_size=512, num_workers=4)
        self.val_dataLoader = DataLoader(SteamDataset(val_dataLoader, self.all_gameIds),batch_size=512, num_workers=4)

        # Saving number of users and items
        self.num_users = matrix['user_id'].max() + 1 
        self.num_items = matrix['game_id'].max() + 1 
        self.matrix = matrix

    def get_features(self, game_id):
        return self.games[self.games['game_id'] == int(game_id)].drop(['game_id', 'publisher', 'price'],axis=1).to_numpy().flatten()

    def get_publisher(self, game_id):
        return self.games[self.games['game_id'] == int(game_id)].iloc[0,1]

    def get_price(self, game_id):
        return self.games[self.games['game_id'] == int(game_id)].iloc[0,2]

    def get_user_interacted_items(self):
        return self.matrix.groupby('user_id')['game_id'].apply(list).to_dict()
