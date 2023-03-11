# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 15:09:08 2023

@author: narut
"""

from topic_transform import interviewbit2leetcode
from interviewbit_data import *
import sys, os
sys.path.insert(0, os.path.join(os.getcwd(), "..", "db"))
from db_operation import create_table, drop_table, insert_row
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager


def setup_tables():
  # create a table for all problems
  problem_cols = [
    "id INT PRIMARY KEY",
    "title_slug VARCHAR(255) UNIQUE NOT NULL",
    "title VARCHAR(255) NOT NULL",
    "difficulty ENUM('Easy', 'Medium', 'Hard') NOT NULL",
    "ac_rate DECIMAL(7, 4)",
    "total_accepted INT UNSIGNED"
  ]
  create_table("interviewbit_problem", problem_cols)
  
  # create a table of company tags of problems
  company_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "company_name VARCHAR(255) NOT NULL"
  ]
  create_table("interviewbit_company", company_cols)
  
  # create a table of topic tags of problems
  topic_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "topic_name VARCHAR(255) NOT NULL"
  ]
  create_table("interviewbit_topic", topic_cols)
  
  # create a table for processed description
  des_cols = [
    "id INT NOT NULL",
    "title_slug VARCHAR(255) NOT NULL",
    "description VARCHAR(15000)"
  ]
  create_table("interviewbit_description", des_cols)
  

if __name__ == "__main__":
  chrome_options = webdriver.ChromeOptions()
  chrome_options.add_argument('--headless')
  chrome_options.add_argument('--no-sandbox')
  chrome_options.headless = True
  wd = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
  
  setup_tables()
  problem_list = fetch_interviewbit_problems()
  
  for idx, problem in enumerate(problem_list):
    ac_rate = get_ac(wd, problem["slug"])
    description = get_description(problem["slug"])
    tag_list = interviewbit2leetcode([problem["topic_title"]])
    if problem["difficulty_level"] == "very_easy":
      difficulty = "easy"
    elif problem["difficulty_level"] == "very_hard":
      difficulty = "hard"
    else:
      difficulty = problem["difficulty_level"]
    
    problem_cols = [
      "id",
      "title_slug",
      "title",
      "difficulty",
      "ac_rate",
      "total_accepted"
    ]
    company_cols = ["id", "title_slug", "company_name"]
    topic_cols = ["id", "title_slug", "topic_name"]
    des_cols = ["id", "title_slug", "description"]
    
    # Insert the record of the current problem
    problem_data = [
      problem["id"],
      problem["slug"],
      problem["problem_statement"],
      difficulty,
      ac_rate,
      problem["solved_by"]
    ]
    insert_row("interviewbit_problem", problem_cols, problem_data)
    # print(problem_data)
    
    # Insert all companies tagged on the current problem
    for company in problem["tags"]:
      company_data = [
        problem["id"],
        problem["slug"],
        company
      ]
      insert_row("interviewbit_company", company_cols, company_data)
    #print(problem["tags"])
    
    # Insert all topics tagged on the current problem
    for topic in tag_list:
      topic_data = [
        problem["id"],
        problem["slug"],
        topic
      ]
      insert_row("interviewbit_topic", topic_cols, topic_data)
    #print(tag_list)
    
    # Insert the processed description into the table
    des_data = [
      problem["id"],
      problem["slug"],
      description
    ]
    insert_row("interviewbit_description", des_cols, des_data)
    #print(description)
    
    
    
    
    