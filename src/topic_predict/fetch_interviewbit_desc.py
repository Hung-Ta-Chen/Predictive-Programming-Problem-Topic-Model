# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 16:41:00 2023

@author: narut
"""

import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "..", "db"))
from db_operation import search_rows


if __name__ == "__main__":
  # Create a directory if it doesn't exist
  if not os.path.exists("../../data/interviewbit_descriptions"):
    os.makedirs("../../data/interviewbit_descriptions")
  
  # Fetch description of all leetcode problems from the database
  problem_list = search_rows("interviewbit_description")
  
  # Write the description of the problem into a new .txt file
  # and write the topics of the problem as a new line in topic_label.txt
  with open("../../data/interviewbit_topics.txt", "w") as f: 
    idx = 0
    for problem in problem_list:
      title = problem[1]
      topic_list = [record[2] for record in search_rows("interviewbit_topic", filters=f"title_slug = \"{title}\"")]
      topic_str = ",".join(topic_list)
      topic_str += "\n"
      
      # Skip those without description or labels
      if topic_str != "\n" and problem[2]:
        with open(f"../../data/interviewbit_descriptions/{idx}.txt", "w", encoding="utf-8") as desc_file:
          desc_file.write(problem[2])
        
        f.write(topic_str)
        idx += 1