# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 16:35:02 2023

@author: narut
"""

from transformers import BertTokenizer
import torch
from torch.utils.data import Dataset
import os


class LeetcodeDataset(Dataset):
  def __init__(self, data_dir, desc_dirname, topic_filename, max_len=256):
    self.desc_dir = os.path.join(data_dir, desc_dirname)
    self.topics_file = os.path.join(data_dir, topic_filename)
    self.max_len = max_len
    with open(self.topics_file, "r") as f:
        self.topics = [line.strip().split(",") for line in f]
    self.tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
  
  def __len__(self):
    return len(self.topics)

  def __getitem__(self, index):
    if index < 0:
      index = len(self.topics) + index
    topics = self.topics[index]
    desc_file = os.path.join(self.desc_dir, f"{index}.txt")
    with open(desc_file, "r") as f:
        desc = f.read()
    # tokenize the description
    encoding = self.tokenizer(desc, max_length=self.max_len, padding='max_length', truncation=True, return_tensors='pt')
    
    # encode the output with one-hot encoding
    all_topics = ["Array", "String", "Hash Table", "Dynamic Programming", "Math",\
                  "Sorting", "Greedy", "Depth-First Search", "Database", "Binary Search",\
                  "Breadth-First Search", "Tree", "Matrix", "Binary Tree", "Two Pointers",\
                  "Bit Manipulation", "Stack", "Heap (Priority Queue)", "Graph", "Prefix Sum",\
                  "Counting", "Backtracking", "Sliding Window", "Union Find", "Linked List",\
                  "Ordered Set", "Monotonic Stack", "Enumeration", "Recursion", "Trie",\
                  "Divide and Conquer", "Binary Search Tree", "Queue", "Bitmask", "Memoization",\
                  "Geometry", "Segment Tree", "Topological Sort", "Number Theory", "Binary Indexed Tree",\
                  "Hash Function", "Game Theory", "Combinatorics", "Shortest Path", "String Matching",\
                  "Rolling Hash", "Monotonic Queue"]
    topic_label = [int(topic in topics) for topic in all_topics]
    
    # return the encoding and corresponding topic
    return {
      "input_ids": encoding["input_ids"].squeeze(0),
      "attention_mask": encoding["attention_mask"].squeeze(0),
      "labels": torch.tensor(topic_label)
    }


if __name__ == "__main__":
  dataset = LeetcodeDataset("../../data/", "leetcode_descriptions", "leetcode_topics.txt")
  print(dataset[1])