# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 14:05:55 2023

@author: narut
"""

from topic_transform import codechef2leetcode
from codechef_data import fetch_codechef_data, fetch_problem_tags_description
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "..", "db"))
from db_operation import create_table, drop_table, insert_row
import re


def get_description(problem_content):
  if not problem_content:
    return None
  
  #content = problem_content.split("Note")[0]
  other_lang = r"(?:### )?Read problem[s]? statements in .+"
  content = re.sub(other_lang, "", problem_content)
  statement = r"(?:Problem )?Statement"
  content = re.sub(statement, "", content)
  if re.search(r"[$][\w_]+[$]", content):
    if re.search(r"###[ ]?Input", content) or re.search(r"###[ ]?INPUT", content) or re.search(r"### Interaction", content):
      description = content.split("###")[0]
    else:
      description = content 
  elif re.search(r"<[^<>]+>", content):
    if re.search(r"<[\w =\":;]+>[\n]*Input[ \n:\w]*<[/][\w =\":;]+>", content):
      description = content.split("Input")[0]
    elif re.search(r"<[\w =\":;]+>[\n]*INPUT[ \n:\w]*<[/][\w =\":;]+>", content):
      description = content.split("INPUT")[0]
    else:
      description = content
  else:
    description = content
     
  description = re.sub(r"[$]", "", description)
  description = re.sub(r"[*]{1,2}([^*]+)[*]{1,2}", r"\1", description)
  tag_pattern = r"<[^<>]+>"
  description = re.sub(tag_pattern, "", description)
  description = re.sub(r"\\leq", "<=", description)
  description = re.sub(r"\\le", "<=", description)
  description = re.sub(r"\\geq", ">=", description)
  description = re.sub(r"\\ge", ">=", description)
  description = re.sub(r"\\neq", "!=", description)
  description = re.sub(r"\\ne", "!=", description)
  return description


def setup_tables():
  # create a table for all problems
  problem_cols = [
    "id INT PRIMARY KEY",
    "title_slug VARCHAR(255) UNIQUE NOT NULL",
    "title VARCHAR(255) NOT NULL",
    "difficulty VARCHAR(255)",
    "diff_rate INT",
    "total_accepted INT UNSIGNED",
    "total_sub INT UNSIGNED"
  ]
  create_table("codechef_problem", problem_cols)
  
  # create a table of topic tags of problems
  topic_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "topic_name VARCHAR(255) NOT NULL",
  ]
  create_table("codechef_topic", topic_cols)
  
  # create a table for processed description
  des_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "description VARCHAR(15000)"
  ]
  create_table("codechef_description", des_cols)


if __name__ == "__main__":
  setup_tables()
  
  problem_list = fetch_codechef_data()
  problem_cols = [
    "id",
    "title_slug",
    "title",
    "difficulty",
    "diff_rate",
    "total_accepted",
    "total_sub"
  ]  
  
  topic_cols = ["id", "title_slug", "topic_name"]
  des_cols = ["id", "title_slug", "description"]
  
  for idx, problem in enumerate(problem_list[:]):
    info = fetch_problem_tags_description(problem["code"])
    difficulty, content, topics = info[0], info[1], info[2]
    
    # Insert the record of each problem
    problem_data = [
      problem["id"],
      problem["code"],
      problem["name"],
      difficulty,
      problem["difficulty_rating"],
      problem["successful_submissions"],
      problem["total_submissions"]
    ]
    insert_row("codechef_problem", problem_cols, problem_data)
    
    # Insert the processed description into the table
    des_data = [
      problem["id"],
      problem["code"],
      get_description(content)
    ]
    insert_row("codechef_description", des_cols, des_data)
    
    # Insert the all topics tagged of the current problem
    transformed_tags = codechef2leetcode(topics)
    for topic in transformed_tags:
      topic_data = [
        problem["id"],
        problem["code"],
        topic
      ]
      insert_row("codechef_topic", topic_cols, topic_data)
    # info = fetch_problem_tags_description(problem["code"])
    # difficulty, content, topics = info[0], info[1], info[2]
    # print(topics)
    # print(codechef2leetcode(topics))

    
    
    
    
    