import configparser
import mysql.connector
import datetime as datetime
import os
from django..urls import include, url, path

# Create a function for fetching data from the database. Should also prevent SQL Injection with use of list parameter
def sql_query(sql, *query_params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor(buffered = True)
    cursor.execute(sql, *query_params)
    result = cursor.fetchall()
    cursor.close()
    db.close()
    return result

def sql_execute(sql, *query_params):
    db = mysql.connector.connect(**config['mysql.connector'])
    cursor = db.cursor(buffered = True)
    cursor.execute(sql, *query_params)
    db.commit()
    cursor.close()
    db.close()

# Queries for creating an account
    # Email
    sql = "select count(email) from user where email = %s"
    query_params = [(session['email'],)]
    count_email = sql_query(sql, *query_params)
    if count_email[0][0] > 0:
        # Handle error if user inputs email that already exists in database

    # Username
    session['username'] = request.form["username"]
    sql = "select count(username) from user where username = %s"
    query_params = [(session['username'],)]
    count_usernames = sql_query(sql, *query_params)
    if count_usernames[0][0] > 0:
        # Handle error if user inputs username that already exists in database

    # Password
    password = request.form["password"]
    sql = "insert into user(username, password, email) values(%s, %s, %s)"
    query_params = [(session['username'], password, session['email'])]
    sql_execute(sql, *query_params)

# Queries for storing stock data
