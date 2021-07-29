import numpy as np
import torch

device = torch.device('cuda:0' if torch.cuda.is_available() else 'cpu')

# Calculating NDCG metric for sorted list and specific item
def getNDCG(rankList, gItem):
    for i in range(len(rankList)):
        item = rankList[i]
        if item == gItem:
            return np.log(2) / np.log(i+2)
    return 0

# Model evaluation
# Input is model, test data and k parameter
def evaluate(model, data, k=10):
    user_interacted_items = data.get_user_interacted_items()
    hits = []
    ndcg = []
    for (u,i) in data.test_user_item_set:
        # Test data preparation and adding negative samples
        interacted_items = user_interacted_items[u]
        not_interacted_items = set(data.all_gameIds) - set(interacted_items)
        selected_not_interacted = list(np.random.choice(list(not_interacted_items), 100))
        test_items = selected_not_interacted + [i]
        
        publisher_id = torch.tensor([data.get_publisher(item) for item in test_items])
        prices = torch.tensor([data.get_price(item) for item in test_items], dtype=torch.float32)
        features = torch.tensor([data.get_features(item) for item in test_items], dtype=torch.float32)

        # Prediction and taking only k best items
        predicted_labels = np.squeeze(model(torch.tensor([u]*101).to(device), 
                                            torch.tensor(test_items).to(device), 
                                            publisher_id.to(device), 
                                            prices.to(device),
                                            features.to(device)
                                            ).cpu().detach().numpy())
        topk_items = [test_items[i] for i in np.argsort(predicted_labels)[::-1][0:k].tolist()]

        # NDCG calculation
        val = getNDCG(topk_items, i)
        ndcg.append(val)

        # Hit Ratio calculation
        if i in topk_items:
            hits.append(1)
        else:
            hits.append(0)
            
    return np.average(hits), np.average(ndcg)
    