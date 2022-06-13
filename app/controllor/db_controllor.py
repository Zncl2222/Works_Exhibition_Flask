import os
import psycopg2

class database:

    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']

    def insert_query(self, table, table_columns, records):
        
        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        f = "("
        for i in range(len(records)):
            if i < len(records)-1:
                f += "%s,"
            else:
                f += "%s"
        f += ")"

        insert_table_query = f"INSERT INTO {table} {table_columns} VALUES {f}" 

        cursor.execute(insert_table_query, records)
        conn.commit()

    def select_query(columns, condition):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        
        select_table_query = f"SELECT {columns} FROM user_records_sgsim {condition}"
        cursor.execute(select_table_query)
        res = cursor.fetchall()
        return res

    def insert_uc_sgsim(self, records):

        table = 'user_records_sgsim'
        table_columns = '(ip_address,date,computation_time,model_len,nR,bw,hs,range,sill,randomseed,model,kernel)'

        self.insert_query(table, table_columns, records)