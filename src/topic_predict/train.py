# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:40:58 2023

@author: narut
"""

import torch
import torch.nn as nn
import os
import random
from torch.utils.data import random_split, DataLoader, Subset
from tqdm import tqdm
from dataset import LeetcodeDataset
from model import LeetCodeTopicModel
import matplotlib.pyplot as plt
from predict import predict, predict_topics, decode_topics
from sklearn.metrics import multilabel_confusion_matrix
import pandas as pd

# Define constants
MAX_LEN = 128
BATCH_SIZE = 32
NUM_CLASSES = 47
LR = 2e-5
EPOCHS = 50
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

def train(num_epochs, train_loader, val_loader, model, optimizer, criterion, device, ckp_dir):
    best_val_loss = float('inf')
    train_losses = []
    val_losses = []
    
    for epoch in range(num_epochs):  
        # set the model to train mode
        model.train()
        
        # keep track of the total loss for this epoch
        train_loss = 0
        
        # initialize progress bar
        train_progress = tqdm(train_loader, desc=f"Epoch {epoch+1}/"+f"{num_epochs}, Train", unit="batch")
        
        # iterate over the batches in the training data loader
        for batch in train_progress:
            
            # get the inputs and targets
            inputs = batch['input_ids'].to(device)
            masks = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            
            # zero out the gradients
            optimizer.zero_grad()
            
            # forward pass
            outputs = model(inputs, masks)
            loss = criterion(outputs, labels.float())
            
            # backward pass
            loss.backward()
            optimizer.step()
            
            # update progress bar with current loss
            train_progress.set_postfix({'loss': loss.item()})
            
            # update the training loss
            train_loss += loss.item()
                 
        # compute the average training loss for this epoch
        train_loss /= len(train_loader)
        train_losses.append(train_loss)
        
        # set the model to evaluation mode
        model.eval()
        
        # initialize progress bar
        val_progress = tqdm(val_loader, desc=f"Epoch {epoch+1}/"+f"{num_epochs}, Val", unit="batch")
        
        # turn off gradient calculation
        with torch.no_grad():
            # keep track of the total validation loss for this epoch
            val_loss = 0
            
            # iterate over the batches in the validation data loader
            for batch in val_progress:
                # get the inputs and targets
                inputs = batch['input_ids'].to(device)
                masks = batch['attention_mask'].to(device)
                labels = batch['labels'].to(device)
                
                # forward pass
                outputs = model(inputs, masks)
                loss = criterion(outputs, labels.float())
                
                # update progress bar with current loss
                val_progress.set_postfix({'loss': loss.item()})
                
                # update the validation loss
                val_loss += loss.item()
            
            # compute the average validation loss for this epoch
            val_loss /= len(val_loader)
            val_losses.append(val_loss)
        
        # print the training and validation loss for this epoch
        print(f"Epoch {epoch + 1}: train_loss={train_loss:.4f}, val_loss={val_loss:.4f}")
        
        #torch.save(model.state_dict(), os.path.join(os.getcwd(), f'/checkpoints/{epoch + 1}.pt'))
        
        # save the model if the validation loss has improved
        if val_loss < best_val_loss:
            torch.save(model.state_dict(), os.path.join(ckp_dir, 'best_model.pt'))
            best_val_loss = val_loss
    
    return train_losses, val_losses
                
                
if __name__ == "__main__":
    # Set random seeds for reproducibility
    random.seed(42)
    torch.manual_seed(42)
    torch.cuda.manual_seed_all(42)

    # Set the directory for checkpoints
    if not os.path.exists("./checkpoints"):
      os.makedirs("./checkpoints")
       
    # Set up the dataset
    dataset = LeetcodeDataset("../../data", "leetcode_descriptions", "leetcode_topics.txt", 128)
    
    # Split the dataset into training and testing sets
    train_size = int(0.8 * len(dataset))
    val_size = int(0.1 * len(dataset))
    test_size = len(dataset) - train_size - val_size
    train_dataset, val_dataset, test_dataset = random_split(dataset, [train_size, val_size, test_size])
    
    # Set up the dataloaders
    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE)
    
    # Set up the model and optimizer
    topic_model = LeetCodeTopicModel(NUM_CLASSES)
    optimizer = torch.optim.Adam(topic_model.parameters(), lr=LR)
    criterion = nn.BCEWithLogitsLoss()
    
    # Set up the device
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    topic_model.to(device)
    
    # # Train the model
    # train_loss, val_loss = train(EPOCHS, train_dataloader, val_dataloader, topic_model, optimizer, criterion, device, "./checkpoints")
    
    # # Plot the learning curve
    # plt.plot(range(len(train_loss)), train_loss, label='Training loss')
    # plt.plot(range(len(train_loss)), val_loss, label='Validation loss')
    # plt.xlabel('Epoch')
    # plt.ylabel('Loss')
    # plt.legend(loc='best')
    # plt.show()
    
    # Load the weight
    checkpoint_path = "./checkpoints_archive/best_model_fin.pt"
    checkpoint = torch.load(checkpoint_path)
    topic_model.load_state_dict(checkpoint)
    
    # Testing
    pred_labels, pred_topics = predict_topics(test_dataloader, topic_model, device)
    
    # Compute the confusion matrix for each class
    true_labels = [data_dict["labels"].numpy().tolist() for data_dict in test_dataset]

    confuse_matrices = multilabel_confusion_matrix(true_labels, pred_labels)
    perf_df = pd.DataFrame(columns=['topic', 'precision', 'recall', 'F1 score'])
    for i in range(confuse_matrices.shape[0]):
      matrix = confuse_matrices[i, :, :]
      precision = matrix[1, 1] / (matrix[1, 1]+matrix[0, 1])
      recall = matrix[1, 1] / (matrix[1, 1]+matrix[1, 0])
      f1 = (2*precision*recall) / (precision+recall)
      perf_df.loc[len(perf_df)] = {'topic':all_topics[i],'precision':precision,'recall':recall,'F1 score':f1}
    perf_df = perf_df.sort_values(by=['F1 score'], ascending=False)

    # Plot the table
    fig, ax = plt.subplots(figsize=(15, 15))
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=perf_df.head(20).values, colLabels=perf_df.columns, loc='center')
    fig.tight_layout()
    plt.show()
    
    
    
