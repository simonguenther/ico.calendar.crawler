import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
import json
sys.path.append('../ico.calendar.crawler')
import Helper
import db_sql
import re
import codecs
import time
from bs4 import BeautifulSoup
from Project import Project
from lxml import etree

class ICOCrawler_Icorating(object):

    baseURL = "http://icorating.com/"
    limit = 0 # how many ICOs should be crawled

    # DID NOT YET FILTER FOR EMPTY SYMBOLS AND STUFF
    def __init__(self):
        pass

    def run(self):
        filename = time.strftime("logs/%d-%m-%Y %H-%M - icolist.icorating.json")
        print time.strftime("[icorating.com] %d-%m-%Y %H:%M:%S ICO Crawler for: icorating.com")        

        html_index = Helper.get_html(self.baseURL)
        rawRows = self.get_calendar_rows(html_index, self.limit)
        print time.strftime("[icorating.com] %d-%m-%Y %H:%M:%S Number of ICOs to crawl: " +str(len(rawRows)))     

        columnSlicedRows = self.get_values_from_rows(rawRows)  
        icos = self.create_project_instance_list(columnSlicedRows)
        ico_dict = Helper.projects_to_list_dictionary(icos)

        Helper.save_dictionary_to_json(filename, ico_dict)
        #Helper.save_dictionary_to_database(Helper.projects_to_list_string_dictionary(icos))
        print time.strftime("[icorating.com] %d-%m-%Y %H:%M:%S Saved ICOs: " +str(len(icos)))     
        print time.strftime("[icorating.com] %d-%m-%Y %H:%M:%S Exiting.")     
        return icos

    def get_calendar_rows(self, html, limit):
        rows = []
        soup = BeautifulSoup(html, "lxml")
        pattern = "ico-projects-table__row\sico-project--(red|green|dgreen|yellow)?\sico-project--hype-(green|red|yellow)?\sico-project--risk-(green|red|yellow)?\sico-project--invest-$"

        count = 1                
        for results in soup.findAll("tr", { "class":re.compile(pattern)}):
            rows.append(results)
            if count >= limit and limit != 0:
                break
            else: 
                count += 1
        return rows

    def get_values_from_rows(self, rows):
        content = []
        for each_row in rows:
            values = []
            for column in each_row.findAll('td'):
                values.append(column)
            content.append(values)
        return content

    def create_project_instance_list(self, columnRows):
        icolist = []

        for i in range(0, len(columnRows)):
            singleRow = columnRows[i]
            ico = Project()

            for x in range(0, len(singleRow)):
                row = singleRow[x]
                #print "row: " + str(row)
                d = etree.HTML(str(row))
                
                name = d.xpath('//td[@class="ico-project-name js-sort-class-name"]/@data-sort')
                description = d.xpath('//td[@class="ico-project-name js-sort-class-name"]/div[@class="visible-xs ico-project-name--description"]/text()')
                start_date = d.xpath('//td[@class="ico-project-date js-sort-class-start"]/@data-sort')
                end_date = d.xpath('//td[@class="ico-project-date js-sort-class-end"]/@data-sort')
                social_media = d.xpath('//td[@class="hidden-sm ico-project-links"]/div')

                if name:
                    ico.setVariable("name", str(name[0]))
                if description:
                    ico.setVariable("description",str(description[0]))
                if start_date:
                    start = str(start_date[0])
                    if start != "TBA":
                        ico.setVariable("start_date", str(start_date[0]))
                if end_date:
                    end = str(end_date[0])
                    if end != "TBA":
                        ico.setVariable("end_date", str(end_date[0]))
                if social_media:
                    for url in social_media:
                        isWebsite = url.xpath('a[@class="ico-project-link--www ico-project-link"]/@href')
                        isBTCtalk = url.xpath('a[@class="ico-project-link--bitcointalk ico-project-link"]/@href') 
                        isTwitter = url.xpath('a[@class="ico-project-link--twitter ico-project-link"]/@href') 
                        isFacebook = url.xpath('a[@class="ico-project-link--facebook ico-project-link"]/@href') 
                        isLinkedIn = url.xpath('a[@class="ico-project-link--linkedin ico-project-link"]/@href') 
                        isTelegram = url.xpath('a[@class="ico-project-link--telegram ico-project-link"]/@href') 
                        isMedium = url.xpath('a[@class="ico-project-link--medium ico-project-link"]/@href') 
                        isInstagram = url.xpath('a[@class="ico-project-link--instagram ico-project-link"]/@href') 
                        isGithub = url.xpath('a[@class="ico-project-link--github ico-project-link"]/@href')
                        isSlack = url.xpath('a[@class="ico-project-link--slack ico-project-link"]/@href')
                        isReddit = url.xpath('a[@class="ico-project-link--reddit ico-project-link"]/@href')

                        if isWebsite:
                            ico.setVariable("website", isWebsite[0])
                        if isFacebook:
                            ico.setVariable("facebook", isFacebook[0])
                        if isGithub:
                            ico.setVariable("github", isGithub[0])
                        if isTwitter:
                            ico.setVariable("twitter", isTwitter[0])
                        if isTelegram:
                            ico.setVariable("telegram", isTelegram[0])
                        if isBTCtalk:
                            ico.setVariable("bitcointalk", isBTCtalk[0])
                        if isLinkedIn:
                            ico.setVariable("linkedin", isLinkedIn[0])
                        if isMedium:
                            ico.setVariable("blog", isMedium[0])
                        if isSlack:
                            ico.setVariable("slack", isSlack[0])
                        if isReddit:
                            ico.setVariable("reddit", isReddit[0])
                        if isInstagram:
                            ico.setVariable("instagram", isInstagram[0])
            # end-for singleRow
            icolist.append(ico)
        # end-for columnRows    
        return icolist
            

                

            