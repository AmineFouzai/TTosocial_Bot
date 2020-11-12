import sys 
from selenium.webdriver import ChromeOptions
sys.path.insert(1,"./src/bot")

from bot import GitHubBot

options=ChromeOptions()
options.add_argument('--disable-notifications')
# options.add_argument('--headless')
app=GitHubBot(login="mail",password="pass",options=options)
app.run(to_follow=False,unfollow=False)