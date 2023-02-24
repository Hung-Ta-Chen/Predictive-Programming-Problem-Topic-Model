# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:42:34 2023

@author: narut
"""

from mysql.connector import MySQLConnection, Error
from db_config import read_db_config


def create_table(table_name, table_cols):
  """
  args:
    table_name: name of the taable you want to create
    table_cols: a list of definition of columns
  """
  # read database configuration
  db_config = read_db_config()
  
  # construct the query
  query = f"CREATE TABLE {table_name} ("
  for idx, col in enumerate(table_cols):
    query += col
    if idx != len(table_cols)-1: 
      query += ", "
    else:
      query += ")"

  with MySQLConnection(**db_config) as conn:
    with conn.cursor() as cursor:
      try:
        cursor.execute(query)
        
        conn.commit()
      except Error as e:
        print('Error:', e)


def drop_table(table_name):
  db_config = read_db_config()
  
  query = f"DROP TABLE {table_name}"
  with MySQLConnection(**db_config) as conn:
    with conn.cursor() as cursor:
      try:
        cursor.execute(query)
        
        conn.commit()
      except Error as e:
        print('Error:', e)


def insert_row(table_name, col_list, data_list):
  db_config = read_db_config()
  
  # construct the query
  query = f"INSERT INTO {table_name} ("
  for idx, col in enumerate(col_list):
    query += col
    if idx != len(col_list)-1:
      query += ","
    else:
      query += ") "
  query += "VALUES ("
  for i in range(len(data_list)):
    query += "%s"
    if i != len(data_list)-1:
      query += ","
    else:
      query += ")"
      
  with MySQLConnection(**db_config) as conn:
    with conn.cursor() as cursor:
      try:
        cursor.execute(query, data_list)
        
        conn.commit()
      except Error as e:
        print('Error:', e)
    
  
  

if __name__ == "__main__":
  create_table("test", ["name VARCHAR(255)", "address VARCHAR(255)"])
  insert_row("test", ["name", "address"],\
             ["Yoel", "Cuba", "fd"])
  