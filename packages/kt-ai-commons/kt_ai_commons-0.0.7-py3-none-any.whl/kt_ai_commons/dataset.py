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
    return sqlio.read_sql_query(sql, conn)
    print("onenavi_train 데이터 불러오기가 완료되었습니다.")