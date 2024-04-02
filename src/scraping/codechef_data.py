# -*- coding: utf-8 -*-
"""
Created on Wed Mar  8 01:41:53 2023

@author: narut
"""
from security import safe_requests


def fetch_codechef_data(page=0, limit=100000, sort_order="asc"):
  url = "https://www.codechef.com/api/list/problems"
  
  params = {
    "page": page,
    "limit": limit,
    "sort_by": "difficulty_rating",
    "sort_order": sort_order,
    "category": "rated"
  }
  
  response = safe_requests.get(url, params=params)
  
  if response.status_code == 200:
    if response.json()["data"]:
      data = response.json()["data"]
      return data
  else:
    print("Failed to fetch data")
    print(response)
    return None
  
  
def fetch_problem_tags_description(title_slug):
  url = f"https://www.codechef.com/api/contests/PRACTICE/problems/{title_slug}"
  response = safe_requests.get(url)
  
  if response.status_code == 200:
    data = response.json()
    tags = []
    if "computed_tags" in data:
      tags.extend(data["computed_tags"])
    if "user_tags" in data:
      tags.extend(data["user_tags"])    
    return (data["category_name"], data["problemComponents"]["statement"], tags)
  else:
    print("Failed to fetch data")
    print(response)
    return None
  
  
if __name__ == "__main__":
  d = fetch_codechef_data()
  for i in range(20):
    print(fetch_problem_tags_description(d[i]["code"]))
