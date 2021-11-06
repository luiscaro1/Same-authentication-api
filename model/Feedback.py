from config.db_config import pg_config
import psycopg2

class FeedbackDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn=psycopg2.connect(connection_url)
#getting all the feedbacks from the db
    def getAllFeedback(self):
        cursor=self.conn.cursor()
        query='select * from "feedback";'
        cursor.execute(query)
        result=[]
        for row in cursor:
            result.append(row)
        return result

    
#Creating a new user
    def addFeedback(self,email,websitedesign, ratedesign, websitefunctionality, ratefunctionality, gameavailable, rategames, generalinformation, rateoverall):
        cursor=self.conn.cursor()
        query='insert into "feedback"(email, websitedesign, ratedesign, websitefunctionality, ratefunctionality, gameavailable, rategames, generalinformation, rateoverall) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) returning fid'
        cursor.execute(query,(email,websitedesign, ratedesign, websitefunctionality, ratefunctionality, gameavailable, rategames, generalinformation, rateoverall,))
        fid=cursor.fetchone()
        self.conn.commit()
        return fid

    def getAvgRates(self):
        cursor = self.conn.cursor()
        query = """
                select avg(ratedesign), avg(ratefunctionality),
                avg(rategames), avg(rateoverall)
                from feedback        
                """
        cursor.execute(query)
        #print(cursor)
        a = cursor.fetchone()
        result = []
        for row in a:
            result.append(float(row))
            
        return result


