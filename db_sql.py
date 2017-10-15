import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import psycopg2
import time

def open_connection():
	conn = psycopg2.connect(database="django_test", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
	print time.strftime("[database] %d-%m-%Y %H:%M:%S Database successfully opened")        	        
	return conn

def insert_in_main(conn,general_obj):
	if check_if_feed_exists(conn,general_obj["name"]) == False:
		query = "INSERT INTO projects_main (name, symbol, website, twitter, youtube, blog, facebook, discord, slack, telegram_ann, github) \
	      VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'  )" % (general_obj["name"],general_obj["symbol"],general_obj["website"] ,general_obj["twitter"],general_obj["youtube"],general_obj["blog"],general_obj["facebook"], general_obj["discord"], general_obj["slack"], general_obj["telegram"], general_obj["github"])
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()

def check_if_feed_exists(conn,feed_url):
	feed_exists = False
	query = "SELECT name FROM projects_main where name='%s'" % feed_url
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	if rows and len(rows)>0:
		feed_exists = True
	return feed_exists
