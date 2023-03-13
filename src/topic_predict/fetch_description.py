# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 15:15:05 2023

@author: narut
"""

import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "..", "db"))
from db_operation import search_rows


if __name__ == "__main__":
  # Create a directory if it doesn't exist
  if not os.path.exists("../../data/leetcode_descriptions"):
    os.makedirs("../../data/leetcode_descriptions")
  
  # Fetch description of all leetcode problems from the database
  problem_list = search_rows("leetcode_description")
  
  # Write the description of the problem into a new .txt file
  # and write the topics of the problem as a new line in topic_label.txt
  with open("../../data/leetcode_topic_labels.txt", "w") as f: 
    for idx, problem in enumerate(problem_list):
      with open(f"../../data/leetcode_descriptions/{idx}.txt", "w", encoding="utf-8") as desc_file:
        desc_file.write(problem[2])
      
      title = problem[1]
      topic_list = [record[2] for record in search_rows("leetcode_topic", filters=f"title_slug = \"{title}\"")]
      topic_str = ",".join(topic_list)
      topic_str += "\n"
      f.write(topic_str)
      