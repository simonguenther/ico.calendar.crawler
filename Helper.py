import urllib
import sys
import json
import codecs
import re
import db_sql
import cfscrape
from bs4 import BeautifulSoup

basic_facebook = r"(http(s)?:\/\/)?(www\.)?facebook\.com\/"
basic_twitter = r"(http(s)?:\/\/)?(www\.)?twitter\.com\/"
basic_github = r"(http(s)?:\/\/)?(www\.)?(github|gitlab)\.com\/"
basic_reddit = r"(http(s)?:\/\/)?(www\.)?reddit\.com\/r\/"
basic_btctalk = r"(http(s)?:\/\/)?(www\.)?bitcointalk\.org\/"
basic_medium = r"(http(s)?:\/\/)?(www\.)?medium\.com\/[@]?"
basic_telegram = r"(http(s)?:\/\/)?(www\.)?(t|telegram)\.me\/"
basic_linkedin = r"(http(s)?:\/\/)?(www\.)?linkedin\.com\/"
basic_instagram = r"(http(s)?:\/\/)?(www\.)?instsagram\.com\/"

# Converts Projects-Instance-List to dictionary 
def projects_to_list_dictionary(projects_list):
    ico_dict = {}
    for i in projects_list:
        if type(i.name) is list:
            ico_dict[i.name[0]] = i.toDict()
        else:
            ico_dict[i.name] = i.toDict_list()
    return ico_dict

# Converts Projects-Instance-List to dictionary 
def projects_to_list_string_dictionary(projects_list):
    ico_dict = {}
    for i in projects_list:
        ico_dict[i.name] = i.toDict()
        #print i.toString()
    return ico_dict

def save_dictionary_to_database(dicc):
    conn = db_sql.open_connection()
    for x in dicc:
       db_sql.insert_in_main(conn,dicc[x])
    conn.close()

#get HTML from link
def get_html(url):
    try:
        return urllib.urlopen(url).read()
    except StandardError as e:
        print "Error getting HTML: " + str(e)

# get HTML from link when protected by cloudfare
def get_html_cloud(url):
    try:
        scraper = cfscrape.create_scraper()
        return scraper.get(url).content
    except StandardError as e:
        print "Error getting HTML: " + str(e)

# load dictionary from JSON-file
def load_dictionary_from_json(file):
    with open (file) as data_file:
        return json.load(data_file)

# save dictionary to JSON-file
def save_dictionary_to_json(path, jsonDump):
	with codecs.open(path,'w','utf-8') as f:
		f.write(json.dumps(jsonDump, indent=3))

# strip common referral at the end of URLs
def strip_refs(single):
    return re.sub(r"\?[ref|fref]+=[a-zA-Z.-]+","", single)

# strip numbers at the end of the URL
def strip_numbers(single):
    return re.sub(r"\/[0-9]+","",single)

# strip btctalk 'noise' at the end of URLs
def strip_btctalk_noise(single):
    return re.sub(r"(;all|\.[0-9|msg|new]+((;prev_next=prev#new)|(;prev_next=next#new))?[#msg[0-9]*]?)", "",single)

# strip domain (check out basic URLs on top of this file)
def strip_domain(domain, single):
    output = re.sub(domain,"",single)
    return output.strip("/")