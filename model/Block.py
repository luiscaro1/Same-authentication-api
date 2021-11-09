from config.db_config import pg_config
import psycopg2


class BlockedDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    

    def blockUser(self, uid, uid2, isblocked):
        cursor = self.conn.cursor()
        query = """insert into blocked (uid, uid2, isblocked) values (%s, %s, %s) 
                   returning bid
                """
        cursor.execute(query, (uid, uid2, isblocked))
        result = cursor.fetchone()
        self.conn.commit()

        return result
    
    #verify if there was already an existing friendship
    def verifyIfBlocked(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                select isblocked
                from blocked
                where uid=%s and uid2=%s
                """
        cursor.execute(query, (uid, uid2))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            result = result[0]
            

            return result

    #block the user again if for some reason the user unblocked them at some point
    def blockAgain(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                UPDATE blocked SET isblocked = True 
                where uid =%s and uid2 =%s
                """
        cursor.execute(query, (uid, uid2))
        self.conn.commit()


    def unblock(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                UPDATE blocked SET isblocked = False 
                where uid =%s and uid2 =%s and isblocked=True
                returning isblocked
                """

        cursor.execute(query, (uid, uid2))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def getallBlocked(self, uid):
        cursor = self.conn.cursor()
        query = """
                select uid2
                from blocked
                where uid=%s and isblocked=true
                """
        cursor.execute(query, (uid,))
        result = cursor.fetchall()
        print(result)
        return result

    def getallBlockedBy(self, uid2):
        cursor = self.conn.cursor()
        query = """
                select uid
                from blocked
                where uid2=%s and isblocked=True
                """
        cursor.execute(query, (uid2,))
        result = cursor.fetchall()
        print(result)
        return result

    def checkIsblocked(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                select isblocked
                from blocked
                where uid=%s and uid2=%s
                or uid=%s and uid2=%s
                """
        cursor.execute(query, (uid, uid2, uid2, uid))
        result = cursor.fetchone()
        if (result is None) or (result[0] == False):
            return False
        else:
            return True
        
    