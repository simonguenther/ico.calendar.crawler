import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import psycopg2
from psycopg2 import errorcodes
import time
import datetime

def open_connection():
	conn = psycopg2.connect(database="django_test", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
	print time.strftime("[database] %d-%m-%Y %H:%M:%S Database successfully opened")    
	return conn

def insert_in_main(conn,general_obj):
	if check_if_feed_exists(conn,general_obj["symbol"]) == False:
		query = "INSERT INTO projects_main (name, symbol, website, twitter, youtube, blog, facebook, discord, slack, telegram_ann, github, description, ico_start_date, ico_end_date,first_insert, last_update, reddit, btctalk_ann, instagram ) \
	      VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s' )" % (general_obj["name"],general_obj["symbol"].upper(),general_obj["website"] ,general_obj["twitter"],general_obj["youtube"], general_obj["blog"], general_obj["facebook"], general_obj["discord"], general_obj["slack"], general_obj["telegram"], general_obj["github"],general_obj["description"], general_obj["start_date"], general_obj["end_date"],datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), general_obj["reddit"], general_obj["bitcointalk"], general_obj["instagram"])
		try:
			cur = conn.cursor()
			cur.execute(query)
			conn.commit()
		except psycopg2.IntegrityError as ex:
			print "Integrity Error: " + str(ex)


def check_if_feed_exists(conn,feed_symbol):
	feed_exists = False
	query = "SELECT name FROM projects_main where symbol='%s'" % feed_symbol.upper()
	try:
		cur = conn.cursor()
		cur.execute(query)
		rows = cur.fetchall()
		if rows and len(rows)>0:
			feed_exists = True
	except psycopg2.InternalError as ex:
		print "Internal Error: " + str(ex) + "\n" + query

	return feed_exists
