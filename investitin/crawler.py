import sys
import json
sys.path.append('../ico.calendar.crawler')
import Helper
import db_sql
import re
import time
from bs4 import BeautifulSoup
from Project import Project

class ICOCrawler_Investitin():

    baseURL = "https://www.investitin.com/ico-calendar/"    

    def __init__(self):
        pass
    
    def check_if_all_cells_are_empty(self, proj):
        skip_list = ["symbol", "website", "name", "whitepaper", "description", "end_date", "start_date", "team"]
        for attr, value in vars(proj).items():
            if attr in skip_list:
                continue
            if value != "":
                return False
        return True

    def run(self):
        filename = time.strftime("./logs/%d-%m-%Y %H-%M - icolist.investin.json")
        filename_empty = time.strftime("./logs/%d-%m-%Y %H-%M - icolist.investin - empty symbols.json")

        print time.strftime("[investitin.com] %d-%m-%Y %H:%M:%S ICO Crawler for: investitin.com/ico-calendar")   
        html_index = Helper.get_html(self.baseURL)
        rawRows = self.get_calendar_rows(html_index)
        contentRows = self.get_values_from_row(rawRows)

        icos = self.create_project_instance(contentRows)
        ico_dict = Helper.projects_to_list_dictionary(icos)
        Helper.save_dictionary_to_json(filename, ico_dict)

        empty_symbols = self.get_empty_symbol_projects(icos)
        empty_symbol_icos = Helper.projects_to_list_dictionary(empty_symbols)
        Helper.save_dictionary_to_json(filename_empty, empty_symbol_icos)

        Helper.save_dictionary_to_database(Helper.projects_to_list_string_dictionary(icos))
        
        print time.strftime("[investitin.com] %d-%m-%Y %H:%M Analyzed ICOs: "+ str(len(icos)))
        print time.strftime("[investitin.com] %d-%m-%Y %H:%M:%S Exiting")   
        return icos

    # Get empty symbol projects for manual fixing
    def get_empty_symbol_projects(self, ico_projects):
        empty = []
        for each in ico_projects:
            if self.check_if_all_cells_are_empty(each):
                continue

            if each.symbol == '' or each.symbol is None:
                empty.append(each)
        return empty

    # Returns raw html code of each ICO-row (ommitting row "1" because its the header)
    def get_calendar_rows(self,html_index):
        rows = []
        pattern = "row-[^1]\d*\s(even|odd)?$"
        soup = BeautifulSoup(html_index,"lxml")
        for results in soup.findAll('tr', {'class':re.compile(pattern)}):
            rows.append(results)
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
                    ico.setVariable("name", link.text)
                    ico.setVariable("website", link["href"])

                # Description
                elif i == 2:
                    ico.setVariable("description", values[i].text)

                # Symbol
                elif i == 3:
                    ico.setVariable("symbol",values[i].text)

                # ICO Start Date
                elif i ==4:
                    ico.setVariable("start_date", values[i].text)

                # ICO End Date
                elif i == 5:
                    ico.setVariable("end_date", values[i].text)

                # Team
                elif i == 6:
                    ico.setVariable("team", values[i].text)

                # Whitepaper URL
                elif i == 7:
                    linkwp = values[i].findNext('a', href=True)["href"]
                    ico.setVariable("whitepaper", linkwp)

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
                            ico.setVariable("facebook",url)
                        elif isGithub:
                            ico.setVariable("github", url)
                        elif isTwitter:
                            ico.setVariable("twitter", url)
                        elif isTelegram:
                            ico.setVariable("telegram", url)
                        elif isBTCtalk:
                            ico.setVariable("bitcointalk", url)
                        elif isLinkedIn:
                            ico.setVariable("linkedin", url)
                        elif "slack" in url:
                            ico.setVariable("slack", url)
#                        else:
#                            pass

            ico_list.append(ico)
        return ico_list