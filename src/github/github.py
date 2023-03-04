import os
import re
import time

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class GitHubBot(Chrome):

        login:str
        password:str
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
         
            if self.connect()==False:
                self.quit()
                quit()
            else:
                pass
            
            if to_follow==True:
                self.follow_developers(
                     start_by=self.trending_developers()
                )
            elif unfollow == True:
                    self.unfollow()
            elif to_follow and unfollow:
                print("cant be both True")
           
            else:
                print("cant be both be False")
        

        def connect(self):
            try:
                self.get(f"https://github.com/login")
                self.find_element(by=By.NAME,value="login").send_keys(self.login)
                self.find_element(by=By.NAME,value="password").send_keys(self.password)
                self.find_element(by=By.NAME,value='commit').click()
                if "Incorrect username or password." in self.page_source :
                    print("Incorrect username or password.")
                    return 
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
            self.execute_script("""document.querySelectorAll('.btn-sm').forEach(btn=>btn.click())""")
        
        def trending_developers(self):
           
            self.get("https://github.com/trending/developers")
            self.follow()
            return [
            developer.text for developer in 
            self.execute_script("""
            return document.querySelectorAll(".Link--secondary")
            """) ]
        
        def follow_developers(self,start_by):
            for index,trending_developer in enumerate(start_by):
                self.get(f"https://github.com/{trending_developer}?tab=followers")
                self.follow()
                if index ==25:
                    break
              
        def unfollow(self,page=1):
                url=f'{self.current_url}/MedAmineFouzai?&page=x&tab=following'.replace("x", f"{page}")
                self.get(url)
                self.execute_script("""document.querySelectorAll('.btn-sm').forEach(btn=>btn.click())""")
                try:
                    if(self.execute_script(""" return document.querySelector("#user-profile-frame > div > div > h3").textContent""")=='You aren’t following anybody.'):
                        return 
                except Exception as e:
                    try:
                        if(self.execute_script(""" return document.querySelector("#user-profile-frame > div > p").textContent""")=='That’s it. You’ve reached the end of\n  your followings.'):
                            return
                    except Exception as e:
                        pass 
                else:
                    self.unfollow(page+1)
                    