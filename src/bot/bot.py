from selenium.webdriver import Chrome,ChromeOptions 
from selenium.common.exceptions import StaleElementReferenceException
import time
import os 
class GitHubBot(Chrome):

        login:str
        password:str
        githubname:str
        def __init__(self,login,password,executable_path='chromedriver', port=0, options=None, service_args=None, desired_capabilities=None, service_log_path=None, chrome_options=None, keep_alive=True):
                self.login=login
                self.password=password
                super().__init__(
                    executable_path=executable_path,
                    port=port, 
                    options=options,
                    service_args=service_args,
                    desired_capabilities=desired_capabilities,
                    service_log_path=service_log_path,
                    chrome_options=chrome_options, 
                    keep_alive=keep_alive)
               

        def run(self,to_follow=None,unfollow=None):
            
            self.connect()
            if to_follow==True:
                self.follow_developers(
                     start_by=self.trending_developers()
                )
            elif unfollow == True:
                    time.sleep(5)
                    self.unfollow()
            elif to_follow and unfollow:
                print("cant be both true")
                raise Exception
            else:
                print("cant be both true")
                raise Exception
           
        def connect(self):
            try:
                self.get(f"https://github.com/login?login={self.login}")
                self.find_element_by_name("password").send_keys(self.password)
                self.find_element_by_name('commit').click()
                if "Incorrect username or password." in self.page_source :
                    print("Incorrect username or password.")
                    return False
                elif "Device verification" in self.page_source:
                    verification_code=input("Enter Verefecation code :")
                    self.find_element_by_name("otp").send_keys(verification_code)
                    self.execute_script("""
                    document.getElementsByClassName("btn btn-primary btn-block")[0].click()
                    """)
            except Exception as e:
                print(e)
            else:
                    print("Connected !")
                    return True 
                

        def follow(self):
            self.execute_script("""document.querySelectorAll('input[value="Follow"]').forEach(btn=>btn.click())""")
        
        def trending_developers(self):
           
            self.get("https://github.com/trending/developers")
            self.follow()
            return [
            developer.text for developer in 
            self.execute_script("""
            return document.querySelectorAll(".link-gray")
            """) ]
        
        def follow_developers(self,start_by):
            for index,trending_developer in enumerate(start_by):
                self.get(f"https://github.com/{trending_developer}?tab=followers")
                self.follow()
                if index ==25:
                    break
              
        def unfollow(self):

                self.execute_script("""
                return document.querySelector("#dashboard > div > div.f6.text-gray.mt-4 > a:nth-child(3)")
                """).click()
                url=self.current_url
                page_number=1
                while "That’s it. You’ve reached the end of your followings." not in self.page_source:
                        self.get(url+f"&page={page_number}")
                        self.execute_script("""document.querySelectorAll('input[value="Unfollow"]').forEach(btn=>btn.click())""")
                        time.sleep(5)
                        page_number=page_number+1
