# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:49:04 2023

@author: narut
"""
import json
import time
import sys, os
from leetcode_data import fetch_leetcode_problems, fetch_problem_company_stat, fetch_problem_content
import re
sys.path.insert(0, os.path.join(os.getcwd(), "..", "db"))
from db_operation import create_table, drop_table, insert_row


def get_description(problem_content):
  # get the description part
  description = problem_content.split("<p>&nbsp;</p>")[0]
  
  # remove pre tag first
  pre_pattern = r"<pre>(?:.*[\n])*.*</pre>"
  description = re.sub(pre_pattern, "", description)
  
  # remove html tags
  tag_pattern = r"<[^<>]*>"
  html_char_dict = {
    "&lt;": "<",
    "&gt;": ">",
    "&nbsp;": " ",
    "&amp;": "&",
    "&quot;": "\"",
    "&apos;": "'",
    "&#60;": "<",
    "&#62;": ">",
    "&#160;": " ",
    "&#38;": "&",
    "&#34;": "\"",
    "&#39;": "'"
  }
  description = re.sub(tag_pattern, "", description)
  for key in html_char_dict:
    description = re.sub(key, html_char_dict[key], description)
  
  # remove some extra whitespace characters
  description = re.sub("[\r\t]", " ", description)
  description = re.sub("[ ]{2,}", " ", description)
  description = re.sub("[\n]{2,}", "\n\n", description)
  description = re.sub("\n ", "\n", description)
  return description


def setup_tables():
  # create a table for all problems
  problem_cols = [
    "id INT PRIMARY KEY",
    "title_slug VARCHAR(255) UNIQUE NOT NULL",
    "problem_id INT NOT NULL",
    "title VARCHAR(255) NOT NULL",
    "difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL",
    "paid_only BOOLEAN",
    "ac_rate DECIMAL(7, 4)",
    "likes INT UNSIGNED",
    "dislikes INT UNSIGNED",
    "total_accepted INT UNSIGNED",
    "total_sub INT UNSIGNED"
  ]
  create_table("leetcode_problem", problem_cols)
  
  # create a table of company tags of problems
  company_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "company_name VARCHAR(255) NOT NULL",
    "company_slug VARCHAR(255) NOT NULL"
  ]
  create_table("leetcode_company", company_cols)
  
  # create a table of topic tags of problems
  topic_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "topic_name VARCHAR(255) NOT NULL",
    "topic_slug VARCHAR(255) NOT NULL"
  ]
  create_table("leetcode_topic", topic_cols)
  
  # create a table for processed description
  des_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "description VARCHAR(15000)"
  ]
  create_table("leetcode_description", des_cols)
  

if __name__ == "__main__":
# =============================================================================
#   Here we fetch the data from using leetcode graphql api,
#   and save the data into local mysql database,
# =============================================================================
  
  setup_tables()
  problem_list = fetch_leetcode_problems()
  problem_cols = [
    "id", 
    "title_slug",
    "problem_id",
    "title",
    "difficulty",
    "paid_only",
    "ac_rate",
    "likes",
    "dislikes",
    "total_accepted",
    "total_sub",
  ]  
  company_cols = ["id", "title_slug", "company_name", "company_slug"]
  topic_cols = ["id", "title_slug", "topic_name", "topic_slug"]
  des_cols = ["id", "title_slug", "description"]
  
  for problem in problem_list:
    problem_stat = fetch_problem_company_stat(problem["titleSlug"])
    stat_dict = json.loads(problem_stat["stats"])
    company_list = problem_stat["companyTags"]   
    problem_content = fetch_problem_content(problem["titleSlug"])
    
    # Insert the record of the current problem
    problem_data = [
      problem["frontendQuestionId"],
      problem["titleSlug"],
      problem["questionId"],
      problem["title"],
      problem["difficulty"],
      problem["paidOnly"],
      problem["acRate"],
      problem["likes"],
      problem["dislikes"],
      stat_dict["totalAcceptedRaw"],
      stat_dict["totalSubmissionRaw"]
    ]
    insert_row("leetcode_problem", problem_cols, problem_data)
    
    # Insert all companies tagged on the current problem
    for company in company_list:
      company_data = [
        problem["frontendQuestionId"],
        problem["titleSlug"],
        company["name"],
        company["slug"]
      ]
      insert_row("leetcode_company", company_cols, company_data)
    
    # Insert all topics tagged on the current problem
    for topic in problem["topicTags"]:
      topic_data = [
        problem["frontendQuestionId"],
        problem["titleSlug"],
        topic["name"],
        topic["slug"]
      ]
      insert_row("leetcode_topic", topic_cols, topic_data)
    
    # Insert the processed description into the table
    des_data = [
      problem["frontendQuestionId"],
      problem["titleSlug"],
      get_description(problem_content)
    ]
    insert_row("leetcode_description", des_cols, des_data)
    
    # Sleep to avoid error 429
    time.sleep(0.1)