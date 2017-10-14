import sys
reload(sys) 
sys.setdefaultencoding( "utf-8" )
import psycopg2

def open_connection():
	conn = psycopg2.connect(database="projects_data", user = "postgres", password = "postgrespass", host = "127.0.0.1", port = "5432")
	print "database successfully opened"
	return conn

def insert_in_main(conn,general_obj):
	if check_if_feed_exists(conn,general_obj["Name"]) == False:
		query = "INSERT INTO projects_main (name, symbol, website, twitter, youtube, blog, facebook, discord, slack, telegram_ann, github) \
	      VALUES ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s'  )" % (general_obj["Name"],general_obj["Symbol"],general_obj["Website"] ,general_obj["Twitter"],general_obj["YouTube"],general_obj["Blog"],general_obj["Facebook"], general_obj["Discord"], general_obj["Slack"], general_obj["Telegram"], general_obj["Github"])
		cur = conn.cursor()
		cur.execute(query)
		conn.commit()

def check_if_feed_exists(conn,feed_url):
	feed_exists = False
	query = "SELECT * FROM projects_main where name='%s'" % feed_url
	cur = conn.cursor()
	cur.execute(query)
	rows = cur.fetchall()
	if rows and len(rows)>0:
		feed_exists = True
	return feed_exists
