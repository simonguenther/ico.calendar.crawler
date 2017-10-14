class Project(object):

    def __init__(self):
        self.name = ""
        self.website = ""
        self.description = ""
        self.symbol = ""
        self.start_date = ""
        self.end_date = ""
        self.team = ""
        self.whitepaper_url = ""
        self.facebook_url = ""
        self.github_url = ""
        self.linkedin_url = ""
        self.slack_url = ""
        self.twitter_url = ""
        self.telegram_url = ""
        self.bitcointalk_url = ""
        self.blog = ""
        #self.else_ = ""

    def toString(self):
        print "\nDebug output for ICO Project Class"
        print "Name: " + self.name 
        print "Website: " + self.website 
        print "Blog: " + self.blog 
        print "Description: " + self.description 
        print "Symbol: "+ self.symbol 
        print "Start Date: "+ self.start_date 
        print "End Date: "+ self.end_date 
        print "Team: " + self.team 
        print "Whitepaper: "+ self.whitepaper_url 
        print "Facebook: " + self.facebook_url 
        print "Github: " + self.github_url 
        print "LinkedIn: " + self.linkedin_url 
        print "Slack: "+ self.slack_url 
        print "Twitter: "+ self.twitter_url 
        print "Telegram: " + self.telegram_url 
        print "BTCTalk: " + self.bitcointalk_url 
        

    def toDict(self):
        dict = {}
        #dict["else" ] = self.else_
        dict["name"] = self.name
        dict["website"] =  self.website
        dict["blog"] = self.blog
        dict["description"] = self.description
        dict["symbol"] = self.symbol
        dict["start_date"] = self.start_date
        dict["end_date"] = self.end_date
        dict["team"] = self.team
        dict["whitepaper"] = self.whitepaper_url
        dict["facebook"] = self.facebook_url
        dict["github"] = self.github_url
        dict["linkedin"] = self.linkedin_url
        dict["slack"] = self.slack_url
        dict["twitter"] = self.twitter_url
        dict["telegram"] = self.telegram_url
        dict["bitcointalk"] = self.bitcointalk_url
        return dict