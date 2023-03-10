# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 16:35:25 2023

@author: narut
"""

import re


def codechef2leetcode(tag_list):
  tag_map = {
    "arrays": "Array",
    "string": "String",
    "string algos": "String",
    "hashmaps": "Hash Table",
    "maps": "Hash Table",
    #"DP": "Dynamic Programming",
    "dynamic programming": "Dynamic Programming",
    "mathematics": "Math",
    "sorting": "Sorting",
    "greedy": "Greedy",
    "advanced greedy": "Greedy",
    "dfs": "Depth-First Search",
    "bfs": "Breadth-First Search",
    "matrices": "Matrix",
    "matrix": "Matrix",
    "fenwick trees": "Binary Indexed Tree",
    "two pointers": "Two Pointers",
    "bit manipulation": "Bit Manipulation",
    "bitwise operation": "Bit Manipulation",
    "stacks": "Stack",
    "heaps": "Heap (Priority Queue)",
    "priority queue": "Heap (Priority Queue)",
    #"Graph": "Graph",
    "prefix sum": "Prefix Sum",
    "simulation": "Simulation",
    "backtracking": "Backtracking",
    "sliding window": "Sliding Window",
    "disjoint set union": "Union Find",
    "dsu": "Union Find",
    "linkedlists": "Linked List",
    "monotonic stack": "Monotonic Stack",
    "enumeration": "Enumeration",
    "recursion": "Recursion",
    "tries": "Trie",
    "tries with xor": "Trie",
    "divide and conquer": "Divide and Conquer",
    "advanced divide and conquer": "Divide and Conquer",
    "queues": "Queue",
    #"Bitmasking": "Bitmask",
    "memoization": "Memoization",
    "computational geometry": "Geometry",
    "geometry": "Geometry",
    "segment trees": "Segment Tree",
    "topological sorting": "Topological Sort",
    "number theory": "Number Theory",
    "hashing": "Hash Function",
    "game theory": "Game Theory",
    "combinatorics": "Combinatorics",
    "shortest paths": "Shortest Path",
    "interactive problems": "Interactive",
    "string matching": "String Matching",
    "rolling hash": "Rolling Hash",
    "randomized algorithms": "Randomized",
    "probability": "Probability and Statistics",
    "expected value": "Probability and Statistics",
    "suffix arrays": "Suffix Array",
    "minimum spanning trees": "Minimum Spanning Tree",
    "strongly connected components": "Strongly Connected Component",
    "biconnected components": "Biconnected Component",
    "binary search": "Binary Search",
    "binary search on answer": "Binary Search",
    "binary tree": "Binary Tree",
    "trees": "Tree",
    "tree algos": "Tree",
    "tree data structure": "Tree",
    "advanced tree structures": "Tree",
    "binary search tree": "Binary Search Tree"
  }
  new_tag_list = set({})
  for tag in tag_list:
    tag = tag.lower()
    tag = tag.replace("-", " ")
    if tag in tag_map:
      new_tag_list.add(tag_map[tag])
    elif tag+'s' in tag_map:
      new_tag_list.add(tag_map[tag+'s'])
      
    if re.search("dp", tag):
      new_tag_list.add("Dynamic Programming")
    if re.search("bitmask", tag):
      new_tag_list.add("Bitmask")
    if re.search("graph", tag):
      new_tag_list.add("Graph")
    if re.search("flow", tag):
      new_tag_list.add("Graph")
    if re.search("bipartite", tag):
      new_tag_list.add("Depth-First Search")
      new_tag_list.add("Breadth-First Search")
      new_tag_list.add("Union Find")
  
  return list(new_tag_list)
  

if __name__ == "__main__":
  print(codechef2leetcode(['acmkgp14', 'admin', 'easy-medium', 'fenwick-tree', 'segment-tree', 'sorting']))
  