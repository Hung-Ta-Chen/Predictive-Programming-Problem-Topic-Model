# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 15:49:04 2023

@author: narut
"""
import json
import time
from leetcode_data import fetch_leetcode_problems, fetch_problem_company_stat, fetch_problem_content

if __name__ == "__main__":
  problem_list = fetch_leetcode_problems()
  company_table = []
  stat_table = []
  content_table = []
  for problem in problem_list:
    problem_stat = fetch_problem_company_stat(problem["titleSlug"])
    stat_dict = json.loads(problem_stat["stats"])
    stat_dict["titleSlug"] = problem["titleSlug"]
    stat_table.append(stat_dict)
    company_list = problem_stat["companyTags"]
    company_table.append({"titleSlug": problem["titleSlug"], "companyTags": company_list})
    
    problem_content = fetch_problem_content(problem["titleSlug"])
    content_table.append({"titleSlug": problem["titleSlug"], "content": problem_content})
    
    # Sleep to avoid error 429
    time.sleep(0.1)