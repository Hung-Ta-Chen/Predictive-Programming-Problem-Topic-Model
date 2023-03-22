#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 22:17:33 2023

@author: windy8810
"""
import mysql.connector
from mysql.connector import MySQLConnection, Error
from db_config import read_db_config
import re
import os
import pandas as pd

#all company name
def company_name():
    query_overall_company_name=("""SELECT DISTINCT company_name FROM interviewbit_company 
                UNION SELECT DISTINCT company_name FROM leetcode_company""")
    return(cursor_execute(query_overall_company_name))
   
#all difficulty
def difficulty():
    query_overall_difficulty=("""(select distinct difficulty from codechef_problem union select distinct difficulty from interviewbit_problem) 
           union select distinct difficulty from leetcode_problem""")
    return(cursor_execute(query_overall_difficulty))

#all topic
def topic():
    query_overall_top_name=("""(select distinct topic_name from codechef_topic union select distinct topic_name from interviewbit_topic) 
        union select distinct topic_name from leetcode_topic""")
    return(cursor_execute(query_overall_top_name))
        

def cursor_execute(x):
    db_config = read_db_config()
    with MySQLConnection(**db_config) as conn:
        with conn.cursor() as cursor:
            try:
                cursor.execute(x)
                results=cursor.fetchall()
                if len(results)>0:
                    rs=pd.DataFrame(results)
                    rs=rs.iloc[:,0].tolist()
                    rs=[i.lower() for i in rs]
                    return rs
                else:
                    return[]
            except Error as e:
                print('Error:', e)
            


           
def recommand_problem_with_company(x,y,z):
    #x=company name  #y=topic name #z=difficulty

    codechef=[]
    interviewbit=[]
    leetcode=[]
    Company=company_name()
    Topic=topic()
    Difficulty=difficulty()
    if Company.count(x.lower())>0 or x!="":
        if y.lower() in Topic and z.lower() in Difficulty:  
            query_interviewbit_proplem=(f"""select distinct title from interviewbit_problem where id in (select distinct id From interviewbit_company where "{x}" in (company_name) 
                    AND EXISTS (select distinct id from interviewbit_topic where "{y}" in (topic_name))
                    AND EXISTS(select distinct id from interviewbit_problem where "{z}" in (difficulty)))""")
            query_leetcode_problem=(f"""select distinct title from leetcode_problem where id in (select distinct id From leetcode_company where "{x}" in (company_name) 
                    AND EXISTS (select distinct id from leetcode_topic where "{y}" in (topic_name)) 
                    AND EXISTS(select distinct id from leetcode_problem where "{z}" in (difficulty)))""")
            interviewbit=cursor_execute(query_interviewbit_proplem)
            leetcode=cursor_execute(query_leetcode_problem)

        elif y.lower() in Topic:
            query_interviewbit_proplem=(f"""select distict title from interviewbit_problem where id in (select distinct id from interviewbit_topic where "{y}" in (topic_name) 
            and exists (select distinct id From interviewbit_company where "{x}" in (company_name)))""")
            query_leetcode_problem=(f"""select title from leetcode_problem where id in (select distinct id from leetcode_topic where "{y}" in (topic_name)and exists 
            (select distinct id From leetcode_company where "{x}" in (company_name)))""")
            interviewbit=cursor_execute(query_interviewbit_proplem)
            leetcode=cursor_execute(query_leetcode_problem)
        
        elif z.lower() in Difficulty:
            query_interviewbit_proplem=(f"""select distinct title from interviewbit_problem where id in (select distinct id from interviewbit_problem where "{z}" in (difficulty) 
            and exists (select distinct id From interviewbit_company where "{x}" in (company_name)))""")
            query_leetcode_problem=(f"""select distinct title from leetcode_problem where id in (select distinct id from leetcode_problem where "{z}" in (difficulty) and exists 
            (select distinct id From leetcode_company where "{x}" in (company_name)))""")
            interviewbit=cursor_execute(query_interviewbit_proplem)
            leetcode=cursor_execute(query_leetcode_problem)
        
                     
    elif y.lower() in Topic and z.lower() in Difficulty:
        query_codechef_problem=(f"""select distinct title from codechef_problem where id in (select distinct id from codechef_topic where "{y}" in (topic_name) 
                        and exists (select distinct id from codechef_problem where "{z}" in (difficulty)))""")
        query_interviewbit_proplem=(f"""select distinct title from interviewbit_problem where id in (select distinct id from interviewbit_topic where "{y}" in (topic_name) 
                        and exists (select distinct id from interviewbit_problem where "{z}" in (difficulty)))""")
        query_leetcode_problem=(f"""select distinct title from leetcode_problem where id in (select distinct id from leetcode_topic where "{y}" in (topic_name) 
                        and exists (select distinct id from leetcode_problem where "{z}" in (difficulty)))""")
        leetcode=cursor_execute(query_leetcode_problem)
        interviewbit=cursor_execute(query_interviewbit_proplem)
        codechef=cursor_execute(query_codechef_problem)


    print(interviewbit,leetcode,codechef)
    return (interviewbit,leetcode,codechef)

def search_problem_in_three_websites():
    x=input("company name")
    y=input("topic type")
    z=input("difficulty")

    a,b,c=recommand_problem_with_company(x,y,z)

    while len(a)==0 or len(b)==0 or len(c)==0: #if no result then restart searching process
        x=input("company name")
        y=input("topic type")
        z=input("difficulty")
        a,b,c=recommand_problem_with_company(x,y,z)

    return(a,b,c)

                        

   
            
          
          
          

          
if __name__ == "__main__":  
    os.chdir(os.getcwd())
    #search_problem_in_three_websites()


    
    

          
          
          
          
          
          
          
          
