import sys 
from selenium.webdriver import ChromeOptions
sys.path.insert(1,"./src/github/")

from github import GitHubBot

options=ChromeOptions()
options.add_argument('--disable-notifications')
# options.add_argument('--headless')
app=GitHubBot(login=sys.argv[0],password=sys.argv[1],options=options)
app.run(to_follow=True,unfollow=False)