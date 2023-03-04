import sys

from selenium.webdriver import ChromeOptions

sys.path.insert(1,"./src/github/")
sys.path.insert(1,"./src/linkedin/")
from github import GitHubBot
from linkedin import LinkedinBot

options=ChromeOptions()
# options.add_argument('--disable-notifications')
# options.add_argument('--headless')
options.add_experimental_option("detach", True)

# gitBot=GitHubBot(login=sys.argv[1],password=sys.argv[2],options=options,keep_alive=True)
# gitBot.run(to_follow=True,unfollow=False)
linkedinBot=LinkedinBot(login=sys.argv[1],password=sys.argv[2],options=options,keep_alive=True)
linkedinBot.run()