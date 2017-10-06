import psycopg2

class HorseDatabase():
    def __init__(self):
        self.conn = None

    def connect(self, host="localhost", dbname="", user="", password=""):
        self.conn = psycopg2.connect("host={} dbname={} user={} password={}".format(host, dbname, user, password))

    def get_conn(self):
        return self.conn