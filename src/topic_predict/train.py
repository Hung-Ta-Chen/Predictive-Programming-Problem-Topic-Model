# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 16:40:58 2023

@author: narut
"""

import torch
import torch.nn as nn
import os
import random
from torch.utils.data import random_split, DataLoader
from tqdm import tqdm
from dataset import LeetcodeDataset
from model import LeetCodeTopicModel


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
    train_progress = tqdm(train_loader, desc=f"Epoch {epoch+1}/"+f"{num_epochs}", unit="batch")
    
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
    val_progress = tqdm(val_loader, desc=f"Epoch {epoch+1}/"+f"{num_epochs}", unit="batch")
    
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


if __name__ == "__main__":
  # Set random seeds for reproducibility
  random.seed(42)
  torch.manual_seed(42)
  torch.cuda.manual_seed_all(42)
  
  # Define constants
  MAX_LEN = 128
  BATCH_SIZE = 32
  NUM_CLASSES = 47
  LR = 2e-5
  EPOCHS = 5
  
  # Set up the dataset
  dataset = LeetcodeDataset("../../data", "leetcode_descriptions", "leetcode_topics.txt", 128)
  
  # Split the dataset into training and validation sets
  train_size = int(0.8 * len(dataset))
  val_size = len(dataset) - train_size
  train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
  
  # Set up the dataloaders
  train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
  val_dataloader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
  
  # Set up the model and optimizer
  topic_model = LeetCodeTopicModel(NUM_CLASSES)
  optimizer = torch.optim.Adam(topic_model.parameters(), lr=LR)
  criterion = nn.BCEWithLogitsLoss()
  
  # Set up the device
  device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
  topic_model.to(device)
  
  # Train the model
  train(EPOCHS, train_dataloader, val_dataloader, topic_model, optimizer, 
        criterion, device, "./checkpoints")
