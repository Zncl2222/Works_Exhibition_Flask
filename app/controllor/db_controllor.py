import os
import psycopg2

class database:

    def __init__(self):
        self.DATABASE_URL = os.environ['DATABASE_URL']
    
    def update_query(self, table, table_columns, val):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        f = "("
        for i in range(len(table_columns)):
            if i < len(table_columns)-1:
                f += "%s,"
            else:
                f += "%s"
        f += ")"

        update_table_query = f"""UPDATE {table} SET {table_columns} = %s;"""
        
        cursor.execute(update_table_query, [val])
    
        conn.commit()

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

    def select_query(self, table, columns, condition):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()
        
        select_table_query = f"SELECT {columns} FROM {table} {condition}"
        cursor.execute(select_table_query)
        res = cursor.fetchall()
        return res

    def insert_uc_sgsim(self, records):

        table = 'user_records_sgsim'
        table_columns = '(ip_address,date,computation_time,model_len,nR,bw,hs,range,sill,randomseed,model,kernel)'

        self.insert_query(table, table_columns, records)

    def select_uc_sgsim_frequency(self):

        table = 'user_records_sgsim'

        table_columns = '(COUNT(id))'
        condition = ""
        
        id_ = self.select_query(table, table_columns, condition)[0][0]

        table_columns = '(COUNT(model))'
        condition = " WHERE model = 'Gaussian' "

        gaussian = self.select_query(table, table_columns, condition)[0][0]

        table_columns = '(COUNT(model))'
        condition = " WHERE model = 'Spherical' "

        spherical = self.select_query(table, table_columns, condition)[0][0]

        table_columns = '(COUNT(kernel))'
        condition = " WHERE kernel = 'Python' "

        python = self.select_query(table, table_columns, condition)[0][0]

        table_columns = '(COUNT(kernel))'
        condition = " WHERE kernel = 'C' "

        c = self.select_query(table, table_columns, condition)[0][0]

        return [id_, gaussian, spherical, python, c]

    def select_uc_sgsim_distincition(self):

        table = 'user_records_sgsim'

        table_columns = '(COUNT(DISTINCT(model_len)))'
        condition = ""
        model_len = self.select_query(table,table_columns,condition)[0][0]

        table_columns = '(COUNT(DISTINCT(nR)))'
        condition = ""
        nR = self.select_query(table,table_columns,condition)[0][0]

        table_columns = '(COUNT(DISTINCT(bw)))'
        condition = ""
        bw = self.select_query(table,table_columns,condition)[0][0]

        table_columns = '(COUNT(DISTINCT(hs)))'
        condition = ""
        hs = self.select_query(table,table_columns,condition)[0][0]

        table_columns = '(COUNT(DISTINCT(range)))'
        condition = ""
        range_ = self.select_query(table,table_columns,condition)[0][0]

        table_columns = '(COUNT(DISTINCT(sill)))'
        condition = ""
        sill = self.select_query(table,table_columns,condition)[0][0]

        table_columns = '(COUNT(DISTINCT(randomseed)))'
        condition = ""
        randomseed = self.select_query(table,table_columns,condition)[0][0]

        return [model_len, nR, bw, hs, range_, sill, randomseed]



class database_visited(database):

    def visited_select(self):

        conn = psycopg2.connect(self.DATABASE_URL, sslmode='require')
        cursor = conn.cursor()

        res = self.select_query('visited', 'counts', '')[0][0]

        return res

    def visited_update(self):

        visited = int(self.visited_select()) + 1

        self.update_query('visited', 'counts', visited)

        
