from config.db_config import pg_config
import psycopg2


class FriendDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn = psycopg2.connect(connection_url)

    
#eventually se tienen que añadir el verification if the user is blocked
    #create new friendship
    def addFriend(self, uid, uid2, isfriend):
        cursor = self.conn.cursor()
        query = """insert into friend (uid, uid2, isfriend) values (%s, %s, %s) 
                   returning fid
                """
        cursor.execute(query, (uid, uid2, isfriend))
        result = cursor.fetchone()
        self.conn.commit()

        return result
    
    #verify if there was already an existing friendship
    def verifyFriendship(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                select isfriend
                from friend
                where uid=%s and uid2=%s
                or uid=%s and uid2=%s
                """
        cursor.execute(query, (uid, uid2, uid2, uid))
        result = cursor.fetchone()
        if result is None:
            return None
        else:
            result = result[0]
            

            return result

    #be friends again if for some reason the unfriended in the past
    def beFriendsAgain(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                UPDATE friend SET isfriend = True 
                where uid =%s and uid2 =%s
                or uid =%s and uid2 =%s
                """
        cursor.execute(query, (uid, uid2, uid2, uid))
        self.conn.commit()


    def unfriend(self, uid, uid2):
        cursor = self.conn.cursor()
        query = """
                UPDATE friend SET isfriend = False 
                where uid =%s and uid2 =%s and isfriend=True
                or uid =%s and uid2 =%s and isfriend=True
                returning isfriend
                """

        cursor.execute(query, (uid, uid2, uid2, uid))
        result = cursor.fetchone()
        self.conn.commit()
        return result

    def getAllFriends(self, uid):
        cursor = self.conn.cursor()
        query = """
                select uid,uid2
                from friend
                where uid=%s or uid2=%s and isfriend=true
                """
        cursor.execute(query, (uid,uid,))
        result = cursor.fetchall()
        return result

    