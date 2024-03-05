# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 17:07:06 2023

@author: narut
"""
import numpy as np
import torch
from torch.utils.data import DataLoader, random_split
from dataset import LeetcodeDataset
from model import LeetCodeTopicModel
import secrets


def predict(test_loader, model, device):
  # set the model to evaluation mode
    model.eval()
    
    predictions = []
    # turn off gradient calculation
    with torch.no_grad():
        
      # iterate over the batches in the test dataloader
      for batch in test_loader:
        # get the inputs and targets
        inputs = batch['input_ids'].to(device)
        masks = batch['attention_mask'].to(device)
        #labels = batch['labels'].to(device)
        
        # forward pass
        logits = model(inputs, masks)
        #preds = torch.sigmoid(outputs)
        
        #predictions.append(outputs)
        # transform the logit to probability
        probs = torch.sigmoid(logits)
        predictions.append(probs.cpu().numpy())

    predictions = np.vstack(predictions)
    #predictions = torch.cat(predictions, dim=0)  
    
    # return the probabilities
    return predictions

  
def decode_topics(encoded_topics):
  all_topics = ["Array", "String", "Hash Table", "Dynamic Programming", "Math",\
    "Sorting", "Greedy", "Depth-First Search", "Database", "Binary Search",\
    "Breadth-First Search", "Tree", "Matrix", "Binary Tree", "Two Pointers",\
    "Bit Manipulation", "Stack", "Heap (Priority Queue)", "Graph", "Prefix Sum",\
    "Counting", "Backtracking", "Sliding Window", "Union Find", "Linked List",\
    "Ordered Set", "Monotonic Stack", "Enumeration", "Recursion", "Trie",\
    "Divide and Conquer", "Binary Search Tree", "Queue", "Bitmask", "Memoization",\
    "Geometry", "Segment Tree", "Topological Sort", "Number Theory", "Binary Indexed Tree",\
    "Hash Function", "Game Theory", "Combinatorics", "Shortest Path", "String Matching",\
    "Rolling Hash", "Monotonic Queue"
  ]

  predicted_topics = []
  
  for encoded_topic in encoded_topics:
    decoded_topics = []
    
    for idx in range(len(encoded_topic)):
      if encoded_topic[idx] == 1:
        decoded_topics.append(all_topics[idx])
        
    predicted_topics.append(decoded_topics)
    
  return predicted_topics

def predict_topics(test_loader, model, device):
  threshold = 0.5
  
  # Get the preducted probability
  probs = predict(test_loader, model, device)
  encoded_topics = np.where(probs >= threshold, 1, 0)
  predicted_topics = decode_topics(encoded_topics)

  return encoded_topics, predicted_topics
  

if __name__ == "__main__":
  # Define constants
  MAX_LEN = 128
  BATCH_SIZE = 32
  NUM_CLASSES = 47

  # Set random seeds for reproducibility
  secrets.SystemRandom().seed(42)
  torch.manual_seed(42)
  torch.cuda.manual_seed_all(42)

  # Set up the model
  topic_model = LeetCodeTopicModel(NUM_CLASSES)
  checkpoint_path = "./checkpoints_archive/best_model_fin.pt"
  checkpoint = torch.load(checkpoint_path)
  topic_model.load_state_dict(checkpoint)

  # Set up the device
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  topic_model.to(device)

  # Set up the test set
  dataset = LeetcodeDataset("../../data", "leetcode_descriptions", "leetcode_topics.txt", 128)
  train_size = int(0.8 * len(dataset))
  val_size = int(0.1 * len(dataset))
  test_size = len(dataset) - train_size - val_size
  train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
  #test_dataset = LeetcodeDataset("../../data", "interviewbit_descriptions", "interviewbit_topics.txt", 128)

  # Set up the test set loader
  test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE)
  true_labels = [data_dict["labels"] for data_dict in test_dataset]

  true_topics = decode_topics(true_labels)
  _, pred_topics = predict_topics(test_dataloader, topic_model, device)
  for i in range(len(true_topics)):
    print(test_dataset.indices[i], ": Predicted: ", pred_topics[i], "     True: ", true_topics[i])
