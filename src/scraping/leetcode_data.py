# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 17:27:52 2023

@author: Hung-Ta Chen
"""

import requests


def fetch_leetcode_problems(difficulty=None, tags=[], companies=[], listId=None, limit=3000):
  # Type of filters:
  # (1) difficulty: "EASY", "MEDIUM", "HARD"
  # (2) tags (as a list, all lowercase, whitespace replaced by dash): "string", "array", "dynamic-programming", etc
  # (3) companies (as a list, all lowercase, whitespace replaced by dash):  "amazon", "goldman-sachs", etc
  # (4) listId: "7p5x763", etc
  
  result = []

  # API endpoint
  url = "https://leetcode.com/graphql"

  # header
  headers = {
  "accept": "/",
  "accept-encoding": "gzip, deflate",
  "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
  "authorization": "",
  "content-length": "711",
  "content-type": "application/json",
  "origin": "https://leetcode.com",
  "random-uuid": "5f06d95e-99cd-345a-2e04-c6ca20eea305",
  "referer": "https://leetcode.com/problemset/all/",
  "sec-ch-ua": '"Not_A Brand";v="99", "Google Chrome";v="109", "Chromium";v="109"',
  "sec-ch-ua-mobile": "?0",
  "sec-ch-ua-platform": "Windows",
  "sec-fetch-dest": "empty",
  "sec-fetch-mode": "cors",
  "sec-fetch-site": "same-origin",
  "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
  "x-csrftoken": "3p4Pak7GLUW74NOoW57KM6yRgeUu9M5Uo4FUEXZER7tMLrgU2E4l21rmSWtLy4CK",
  "cookie": "gr_user_id=dc56abf1-c003-4fee-a01b-73ec796759bc; __stripe_mid=8d552856-539d-4a18-9ac8-a2110c7cae65eac4af; 87b5a3c3f1a55520_gr_last_sent_cs1=Marvellous-Misadventures-of-Me; csrftoken=3p4Pak7GLUW74NOoW57KM6yRgeUu9M5Uo4FUEXZER7tMLrgU2E4l21rmSWtLy4CK; NEW_PROBLEMLIST_PAGE=1; _gid=GA1.2.39942973.1676071407; __atuvc=1%7C5%2C1%7C6%2C5%7C7; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjk2NzI1NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjliZGQxNjY2ZmY2NGFjYWVlZTZlNDg2NDJmNzllMDQ1NDU3ODQ2YzYiLCJpZCI6Njk2NzI1NiwiZW1haWwiOiJodGNjaGVuQHVjZGF2aXMuZWR1IiwidXNlcm5hbWUiOiJNYXJ2ZWxsb3VzLU1pc2FkdmVudHVyZXMtb2YtTWUiLCJ1c2VyX3NsdWciOiJNYXJ2ZWxsb3VzLU1pc2FkdmVudHVyZXMtb2YtTWUiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2Nzc5Njk1Mi5wbmciLCJyZWZyZXNoZWRfYXQiOjE2NzYxODg0OTQsImlwIjoiMTY4LjE1MC4xMDAuOTEiLCJpZGVudGl0eSI6ImE4MThhYjM1OTgwNDUxN2YyNTQ5ZTk0Yzg4ZDAzYzBiIiwiX3Nlc3Npb25fZXhwaXJ5IjoxMjA5NjAwLCJzZXNzaW9uX2lkIjozMzU1MjkyOX0.wfJ3eA6pLWO8xmSNC1D3AS0AcZBMCmF6j4Lk_nnPdIM; 87b5a3c3f1a55520_gr_session_id=0355fb46-cf9a-4883-8002-8f3565ff2b5a; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=0355fb46-cf9a-4883-8002-8f3565ff2b5a; 87b5a3c3f1a55520_gr_session_id_0355fb46-cf9a-4883-8002-8f3565ff2b5a=true; 87b5a3c3f1a55520_gr_cs1=Marvellous-Misadventures-of-Me; _ga=GA1.1.1007725375.1659092762; _ga_CDRWKZTDEX=GS1.1.1676332840.149.1.1676334999.0.0.0"
  }

  query = """
  query problemsetQuestionList($categorySlug: String, $limit: Int, $skip: Int, $filters: QuestionListFilterInput) {
    problemsetQuestionList: questionList(
      categorySlug: $categorySlug
      limit: $limit
      skip: $skip
      filters: $filters
    ) {
      total: totalNum
      questions: data {
        acRate
        difficulty
        freqBar
        questionId
        frontendQuestionId: questionFrontendId
        isFavor
        paidOnly: isPaidOnly
        likes
        dislikes
        status
        title
        titleSlug
        topicTags {
          name
          id
          slug
        }
        hasSolution
        hasVideoSolution
      }
    }
  }
  """
  
  # 403 error occurs when the returned result is too long
  # So we have to partition the orginal request into several smaller requests
  iter_num = limit // 100 + 1

  for iter in range(iter_num):
    # Filters in the variable part
    filters = {}
    if difficulty: filters["difficulty"] = difficulty
    if tags: filters["tags"] = tags
    if companies: filters["companies"] = companies
    if listId: filters["listId"] = listId
    
    variables = {"categorySlug": "", "skip": 100*iter, "limit": 100, "filters": filters}
    
    # Send the request
    response = requests.post(url, json={'query': query, "variables": variables}, headers=headers)
    
    if response.status_code == 200:
      if response.json()["data"]["problemsetQuestionList"]:
        data = response.json()["data"]["problemsetQuestionList"]["questions"]
        result.extend(data)
    else:
      print("Failed to fetch data")
      print(response)
      return None
  if limit > len(result):
    return result
  else:
    return result[:limit]


def fetch_problem_company_stat(title):
  # API endpoint
  url = "https://leetcode.com/graphql"

  # Header
  headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "",
    "content-length": "230",
    "content-type": "application/json",
    "cookie": "gr_user_id=dc56abf1-c003-4fee-a01b-73ec796759bc; __stripe_mid=8d552856-539d-4a18-9ac8-a2110c7cae65eac4af; 87b5a3c3f1a55520_gr_last_sent_cs1=Marvellous-Misadventures-of-Me; csrftoken=3p4Pak7GLUW74NOoW57KM6yRgeUu9M5Uo4FUEXZER7tMLrgU2E4l21rmSWtLy4CK; __atuvc=1%7C5%2C1%7C6%2C5%7C7; NEW_PROBLEMLIST_PAGE=1; _gid=GA1.2.34307141.1676762278; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjk2NzI1NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjliZGQxNjY2ZmY2NGFjYWVlZTZlNDg2NDJmNzllMDQ1NDU3ODQ2YzYiLCJpZCI6Njk2NzI1NiwiZW1haWwiOiJodGNjaGVuQHVjZGF2aXMuZWR1IiwidXNlcm5hbWUiOiJNYXJ2ZWxsb3VzLU1pc2FkdmVudHVyZXMtb2YtTWUiLCJ1c2VyX3NsdWciOiJNYXJ2ZWxsb3VzLU1pc2FkdmVudHVyZXMtb2YtTWUiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2Nzc5Njk1Mi5wbmciLCJyZWZyZXNoZWRfYXQiOjE2NzY3NjY2MjksImlwIjoiMTY4LjE1MC45Ny44OCIsImlkZW50aXR5IjoiYTgxOGFiMzU5ODA0NTE3ZjI1NDllOTRjODhkMDNjMGIiLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDAsInNlc3Npb25faWQiOjMzNTUyOTI5fQ.bqI_lTf0GoYnG6CJKYulmngfIV5X07s7FkHkPxbk6uQ; 87b5a3c3f1a55520_gr_session_id=edcadcd0-40a8-412d-88c5-1e3fa0317551; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=edcadcd0-40a8-412d-88c5-1e3fa0317551; 87b5a3c3f1a55520_gr_session_id_edcadcd0-40a8-412d-88c5-1e3fa0317551=true; _gat=1; __stripe_sid=c1e9531f-9fa2-4bf5-9b2e-e7046df049b7186a07; 87b5a3c3f1a55520_gr_cs1=Marvellous-Misadventures-of-Me; _ga=GA1.1.1007725375.1659092762; _ga_CDRWKZTDEX=GS1.1.1676838178.159.1.1676839895.0.0.0",
    "origin": "https://leetcode.com",
    "random-uuid": "5f06d95e-99cd-345a-2e04-c6ca20eea305",
    "referer": f"https://leetcode.com/problems/{title}/",
    "sec-ch-ua": 'Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "x-csrftoken": "3p4Pak7GLUW74NOoW57KM6yRgeUu9M5Uo4FUEXZER7tMLrgU2E4l21rmSWtLy4CK"
  }

  # Query
  query = """
    query questionDetailCompanyTags($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        stats
        companyTags {
          name
          slug
          imgUrl
        }
      }
    }   
  """
  variables = {"titleSlug": title}

  # Send the request
  response = requests.post(url, json={'query': query, "variables": variables}, headers=headers)

  if response.status_code == 200:
    data = response.json()["data"]["question"]
    return data
  else:
    print("Failed to fetch data")
    print(response)
    return None


def fetch_problem_content(title):
  # API endpoint
  url = "https://leetcode.com/graphql"

  # Header
  headers = {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate",
    "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "authorization": "",
    "content-length": "187",
    "content-type": "application/json",
    "cookie": "gr_user_id=dc56abf1-c003-4fee-a01b-73ec796759bc; __stripe_mid=8d552856-539d-4a18-9ac8-a2110c7cae65eac4af; 87b5a3c3f1a55520_gr_last_sent_cs1=Marvellous-Misadventures-of-Me; csrftoken=3p4Pak7GLUW74NOoW57KM6yRgeUu9M5Uo4FUEXZER7tMLrgU2E4l21rmSWtLy4CK; __atuvc=1%7C5%2C1%7C6%2C5%7C7; NEW_PROBLEMLIST_PAGE=1; _gid=GA1.2.34307141.1676762278; LEETCODE_SESSION=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJfYXV0aF91c2VyX2lkIjoiNjk2NzI1NiIsIl9hdXRoX3VzZXJfYmFja2VuZCI6ImFsbGF1dGguYWNjb3VudC5hdXRoX2JhY2tlbmRzLkF1dGhlbnRpY2F0aW9uQmFja2VuZCIsIl9hdXRoX3VzZXJfaGFzaCI6IjliZGQxNjY2ZmY2NGFjYWVlZTZlNDg2NDJmNzllMDQ1NDU3ODQ2YzYiLCJpZCI6Njk2NzI1NiwiZW1haWwiOiJodGNjaGVuQHVjZGF2aXMuZWR1IiwidXNlcm5hbWUiOiJNYXJ2ZWxsb3VzLU1pc2FkdmVudHVyZXMtb2YtTWUiLCJ1c2VyX3NsdWciOiJNYXJ2ZWxsb3VzLU1pc2FkdmVudHVyZXMtb2YtTWUiLCJhdmF0YXIiOiJodHRwczovL2Fzc2V0cy5sZWV0Y29kZS5jb20vdXNlcnMvYXZhdGFycy9hdmF0YXJfMTY2Nzc5Njk1Mi5wbmciLCJyZWZyZXNoZWRfYXQiOjE2NzY3NjY2MjksImlwIjoiMTY4LjE1MC45Ny44OCIsImlkZW50aXR5IjoiYTgxOGFiMzU5ODA0NTE3ZjI1NDllOTRjODhkMDNjMGIiLCJfc2Vzc2lvbl9leHBpcnkiOjEyMDk2MDAsInNlc3Npb25faWQiOjMzNTUyOTI5fQ.bqI_lTf0GoYnG6CJKYulmngfIV5X07s7FkHkPxbk6uQ; 87b5a3c3f1a55520_gr_session_id=edcadcd0-40a8-412d-88c5-1e3fa0317551; 87b5a3c3f1a55520_gr_last_sent_sid_with_cs1=edcadcd0-40a8-412d-88c5-1e3fa0317551; 87b5a3c3f1a55520_gr_session_id_edcadcd0-40a8-412d-88c5-1e3fa0317551=true; _gat=1; __stripe_sid=c1e9531f-9fa2-4bf5-9b2e-e7046df049b7186a07; 87b5a3c3f1a55520_gr_cs1=Marvellous-Misadventures-of-Me; _ga=GA1.1.1007725375.1659092762; _ga_CDRWKZTDEX=GS1.1.1676838178.159.1.1676839895.0.0.0",
    "origin": "https://leetcode.com",
    "random-uuid": "5f06d95e-99cd-345a-2e04-c6ca20eea305",
    "referer": f"https://leetcode.com/problems/{title}/",
    "sec-ch-ua": 'Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
    "x-csrftoken": "3p4Pak7GLUW74NOoW57KM6yRgeUu9M5Uo4FUEXZER7tMLrgU2E4l21rmSWtLy4CK"
  }
  
  query = """
    query questionContent($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        content
      }
    }  
  """
  variables = {"titleSlug": title}
  
  # Send the request
  response = requests.post(url, json={'query': query, "variables": variables}, headers=headers)

  if response.status_code == 200:
    data = response.json()["data"]["question"]
    return data["content"]
  else:
    print("Failed to fetch data")
    print(response)
    return None

 
if __name__ == "__main__":
  problem_list = fetch_leetcode_problems()
  for i in range(5):
    print(fetch_problem_content(problem_list[i]["titleSlug"]))
