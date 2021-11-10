from config.db_config import pg_config
import psycopg2


class ReportDAO:
    def __init__(self):
        connection_url="dbname=%s user=%s password=%s host=%s" %(pg_config['dbname'],
                                                                   pg_config['username'],
                                                                   pg_config['password'],
                                                                   pg_config['host'])
        self.conn = psycopg2.connect(connection_url)


    def reportUser(self, uid, uid2,stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending):
        cursor = self.conn.cursor()
        query = """insert into report (uid, uid2, stalking,spamming,
        offensive,harrasment,discrimination,viruses,violationofIP,pretending) values (%s, %s, %s,%s,%s,%s,%s,%s,%s,%s) 
                   returning rid
                """
        cursor.execute(query, (uid, uid2, stalking,spamming,offensive,harrasment,discrimination,viruses,violationofIp,pretending))
        result = cursor.fetchone()
        self.conn.commit()

        return result

#ONLY ADMIN
    def getallReports(self):
        cursor = self.conn.cursor()
        query = """
                select *
                from report
                """
        cursor.execute(query)
        result = cursor.fetchall()
        print(result)
        return result

    
        
    