import re
import requests
import praw
from lxml import html

USERAGENT = "DeckListBot v1.0 by"
USERNAME = "DeckListBot"
PASSWORD = ""
MAXPOSTS = 100
SEARCH_STRING = r'hearthpwn\.com/decks/\d{1,6}.*'

#logging into to Reddit using the bot username and password
reddit = praw.Reddit(USERAGENT)
reddit.login(USERNAME, PASSWORD)

#getting the link from user comments using regular expressions
def get_link(text):
    url = 'http://www.' + re.findall(SEARCH_STRING, text)[0]
    return url

#go to the specific subreddit
#parse the html file for the text we are looking for. In this case card names
#output reponse in comment made by reddit bot
def reply_to_comment():
    subreddit = reddit.get_subreddit("DeckListBotTestArea")
    comments = subreddit.get_comments(limit = MAXPOSTS)
    for comment in comments:
        url = get_link(comment.body)
        r = requests.get(url)
        page = html.fromstring(r.text)
        #print "Working"
        response = ""
        for row in page.xpath("//td[@class='col-name']"):
            #print row[0][0].text + row.xpath('/b')
            name = row.xpath('./b/a/text()')[0]
            mult = row.xpath('./text()')[1].replace('\n', '').replace('\r','').replace(u'\xd7','x')
            # Build the response string
            response += name + " " + mult + "\n\n"
        comment.reply(response)

reply_to_comment()
