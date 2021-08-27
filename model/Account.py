from config.db_config import pg_config
import psycopg2

class AccountDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn=psycopg2.connect(connection_url)

    def getAllUsers(self):
        cursor=self.conn.cursor()
        query="select id, email from test;"
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(row)
        return result