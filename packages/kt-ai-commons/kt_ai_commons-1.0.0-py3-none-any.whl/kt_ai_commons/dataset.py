import psycopg2
import pandas as pd
import pandas.io.sql as sqlio

def onenavi_train():
    conn = psycopg2.connect(host='211.253.10.76', dbname='postgres',user='postgres',password='commons1234!',port=5432)
    cur=conn.cursor()
    sql="""
        SELECT *
        FROM onenavi_train
        ;
        """
    print("onenavi_train 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)

def onenavi_evaluation():
    conn = psycopg2.connect(host='211.253.10.76', dbname='postgres',user='postgres',password='commons1234!',port=5432)
    cur=conn.cursor()
    sql="""
        SELECT *
        FROM onenavi_evaluation
        ;
        """
    print("onenavi_evaluation 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)

def onenavi_pnu():
    conn = psycopg2.connect(host='211.253.10.76', dbname='postgres',user='postgres',password='commons1234!',port=5432)
    cur=conn.cursor()
    sql="""
        SELECT *
        FROM onenavi_pnu
        ;
        """
    print("onenavi_pnu 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)

def onenavi_signal():
    conn = psycopg2.connect(host='211.253.10.76', dbname='postgres',user='postgres',password='commons1234!',port=5432)
    cur=conn.cursor()
    sql="""
        SELECT *
        FROM onenavi_signal
        ;
        """
    print("onenavi_signal 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)

def onenavi_weather():
    conn = psycopg2.connect(host='211.253.10.76', dbname='postgres',user='postgres',password='commons1234!',port=5432)
    cur=conn.cursor()
    sql="""
        SELECT *
        FROM onenavi_weather
        ;
        """
    print("onenavi_weather 데이터 불러오기가 완료되었습니다.")
    return sqlio.read_sql_query(sql, conn)