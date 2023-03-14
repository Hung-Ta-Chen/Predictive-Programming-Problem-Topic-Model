# -*- coding: utf-8 -*-
"""
Created on Mon Mar 13 15:49:08 2023

@author: narut
"""

import torch
import torch.nn as nn
from transformers import BertModel


class LeetCodeTopicModel(nn.Module):
  def __init__(self, num_topics, max_length=256):
    super().__init__()
    self.max_length = max_length
    self.num_topics = num_topics
    self.bert = BertModel.from_pretrained("bert-base-uncased")
    self.dropout = torch.nn.Dropout(0.2)
    self.classifier = nn.Linear(self.bert.config.hidden_size, num_topics)

  def forward(self, input_ids, attention_mask):
    # encode the input sequence with BERT
    outputs = self.bert(input_ids=input_ids, attention_mask=attention_mask)
    last_hidden_state = outputs.last_hidden_state
    # take the mean of the last hidden states as the description embedding
    description_embedding = torch.mean(last_hidden_state, dim=1)
    # use dropout to prevent overfitting
    description_embedding = self.dropout(description_embedding)
    # classify the description embedding into the topics
    logits = self.classifier(description_embedding)
    return logits