import sys
import json
#sys.path.insert(0, '../')
sys.path.append('../ico.calendar.crawler')
import Helper
import db_sql
import re
import time
from bs4 import BeautifulSoup
from Project import Project

class ICOCrawler_Investitin():

    baseURL = "https://www.investitin.com/ico-calendar/"    
    #html_index = ""

    def __init__(self):
        pass
    
    def run(self):
        
        html_index = Helper.get_html(self.baseURL)
        rawRows = self.get_calendar_rows(html_index)
        contentRows = self.get_values_from_row(rawRows)
        icos = self.create_project_instance(contentRows)
        print time.strftime("%d-%m-%Y %H:%M ICO Crawler for: Investinin.com/ico-calendar")        
        print time.strftime("%d-%m-%Y %H:%M Analyzed ICOs: "+ str(len(icos)))
        filename = time.strftime("%d-%m-%Y - icolist.investin.json")

        ico_dict = self.projects_to_dictionary(icos)
        Helper.save_dictionary_to_json(filename, ico_dict)

    # Converts Projects-Instance-List to dictionary 
    def projects_to_dictionary(self, projects_list):
        ico_dict = {}
        for i in projects_list:
            ico_dict[i.name] = i.toDict()
            #print i.toString()
        return ico_dict

    # Returns raw html code of each ICO-row (ommitting row "1" because its the header)
    def get_calendar_rows(self,html_index):
        rows = []
        pattern = "row-[^1]\d*\s(even|odd)?$"
        soup = BeautifulSoup(html_index,"lxml")
        count = 0
        for results in soup.findAll('tr', {'class':re.compile(pattern)}):
            #if count == 0 or count== 1:
            count +=1
            #    continue
            rows.append(results)
            
            count +=1

        return rows

    # Slice ICO-row-content into pieces ==> relevant data, but still with unprocessed HTML tags
    # Returns array in array:
    #   ==> main array: all rows
    #   ==> sub array: each column for a row
    def get_values_from_row(self, content):
        ICOcontent = []
        for each_content in content:
            values = [""]
            for single in each_content.findAll('td', {'class':re.compile('column-[0-9]+')}):
                values.append(single)
            ICOcontent.append(values)
        return ICOcontent

    # Cuts HTML-tags and create ICO-Project instance
    def create_project_instance(self, rawColumns):
        ico_list = []

        for x in range (0, len(rawColumns)):
            values = []
            values = rawColumns[x]
            ico = Project()
            processed = []

            for i in range (1,len(values)):
                # Name and Link to Website
                if i == 1:
                    link = values[i].findNext('a', href=True)
                    ico.name = link.text
                    #print "Analyzing: " + ico.name
                    ico.website = link["href"]
                    #print " ========= " + ico.name + " ========= "
                # Description
                elif i == 2:
                    ico.description = values[i].text.encode("utf-8")

                # Symbol
                elif i == 3:
                    ico.description = values[i].text

                # ICO Start Date
                elif i ==4:
                    ico.start_date = values[i].text

                # ICO End Date
                elif i == 5:
                    ico.end_date = values[i].text

                # Team
                elif i == 6:
                    ico.team = values[i].text.encode("utf-8")

                # Whitepaper URL
                elif i == 7:
                    ico.whitepaper_url = values[i].findNext('a', href=True)["href"]

                # Social Media Channels by domain
                elif i >= 8:
                    
                    url = values[i].findNext('a', href=True)["href"]
                    if url and url not in processed:
                        processed.append(url)
                        isFacebook = re.match(Helper.basic_facebook, url)    
                        isGithub = re.match(Helper.basic_github, url)
                        isTwitter = re.match(Helper.basic_twitter, url)
                        isTelegram = re.match(Helper.basic_telegram, url)
                        isBTCtalk = re.match(Helper.basic_btctalk, url)
                        isLinkedIn = re.match(Helper.basic_linkedin, url)

                        if isFacebook:
                            #print "facebook " + url
                            ico.facebook_url = Helper.strip_domain(Helper.basic_facebook, url)
                        elif isGithub:
                            #print "github " + url
                            ico.github_url = Helper.strip_domain(Helper.basic_github, url)
                        elif isTwitter:
                            #print "twitter " + url
                            ico.twitter_url = Helper.strip_domain(Helper.basic_twitter, url)
                        elif isTelegram:
                            #print "telegram " + url
                            ico.telegram_url = Helper.strip_domain(Helper.basic_telegram, url)
                        elif isBTCtalk:
                            #print "btctalk "  + url
                            url = Helper.strip_btctalk_noise(url)
                            ico.bitcointalk_url = Helper.strip_domain(Helper.basic_btctalk, url)
                        elif isLinkedIn:
                            #print "linkedin " + url
                            ico.linkedin_url = Helper.strip_domain(Helper.basic_linkedin, url)
                        elif "slack" in url:
                            #print "slack " + url
                            ico.slack_url = url
                        else:
                            # Problem here is the probably the findNext-method
                            # as it also uses the html code and finds next url usually website from next project?!
                            pass
                            #print "\telse: " + url
                            #ico.else_ = url

            ico_list.append(ico)
        return ico_list