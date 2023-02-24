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
    

def search_rows(table_name, col_list=["*"], filters=""):
  """
  args:
    table_name: name of the taable you want to create
    col_list: a list of target columns
    filters: a string of the filters
  """
  db_config = read_db_config()
  
  # construct the query
  query = "SELECT "
  for idx, col in enumerate(col_list):
    query += col
    if idx != len(col_list)-1:
      query += ","
    else:
      query += " "
  query += f"FROM {table_name} WHERE {filters}"
  
  with MySQLConnection(**db_config) as conn:
    with conn.cursor() as cursor:
      try:
        cursor.execute(query)   
        
        for record in cursor.fetchall():
          yield record
          
      except Error as e:
        print('Query:', query)
        print('Error:', e)


def search_rows_g(table_name, col_list=["*"], filters="", size=100):
  """
  args:
    table_name: name of the taable you want to create
    col_list: a list of target columns
    filters: a string of the filters
  """
  # define the generator function for reading a limited number of rows at once
  def read_data(cursor, size):
    while True:
      rows = cursor.fetchmany(size)
      if not rows:
        break
      for row in rows:
        yield row
      
  db_config = read_db_config()
  
  # construct the query
  query = "SELECT "
  for idx, col in enumerate(col_list):
    query += col
    if idx != len(col_list)-1:
      query += ","
    else:
      query += " "
  query += f"FROM {table_name} WHERE {filters}"
  
  with MySQLConnection(**db_config) as conn:
    with conn.cursor() as cursor:
      try:
        cursor.execute(query)   
        
        for record in read_data(cursor, size):
          yield record
          
      except Error as e:
        print('Error:', e)
  

def delete_rows(table_name, filters=""):
  db_config = read_db_config()
  
  query = f"DELETE FROM {table_name} WHERE {filters}"
  
  with MySQLConnection(**db_config) as conn:
    with conn.cursor() as cursor:
      try:
        cursor.execute(query)   
        conn.commit()
          
      except Error as e:
        print('Error:', e)
  
  
if __name__ == "__main__":
  # create_table("test", ["name VARCHAR(255)", "country VARCHAR(255)"])
  # insert_row("test", ["name", "country"], ["Yoel Romero", "Cuba"])
  # insert_row("test", ["name", "country"], ["Cael Sanderson", "US"])
  # insert_row("test", ["name", "country"], ["Jordan Burroughs", "US"])
  # insert_row("test", ["name", "country"], ["Kyle Dake", "US"])
  # insert_row("test", ["name", "country"], ["Bo Nickal", "US"])
  # insert_row("test", ["name", "country"], ["Henry Cejudo", "US"])
  # insert_row("test", ["name", "country"], ["Saitiev Adam", "Russia"])

  for i in search_rows_g("test", filters="country = 'US'"):
    print(i)
    
  delete_rows("test", "name='Kyle Dake'")
  
  for i in search_rows_g("test", filters="country = 'US'"):
    print(i)
  