from selenium.webdriver import Chrome,ChromeOptions 
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException
import time
import os 
import re
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
                self.quit()
            elif unfollow == True:
                    time.sleep(5)
                    self.unfollow()
                    self.quit()
            elif to_follow and unfollow:
                print("cant be both True")
                self.quit()
            else:
                print("cant be both be False")
                self.quit()

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
               
                while self.execute_script("""
                return document.querySelector("#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div:nth-child(2) > div > p")
                """) == None:
                        
                        self.get(url+f"&page={page_number}")
                        self.execute_script("""document.querySelectorAll('input[value="Unfollow"]').forEach(btn=>btn.click())""")
                        time.sleep(5)
                        page_number=page_number+1
                        try:
                            if  bool(re.match(self.execute_script("""
                            return document.querySelector("#js-pjax-container > div.container-xl.px-3.px-md-4.px-lg-5 > div > div.flex-shrink-0.col-12.col-md-9.mb-4.mb-md-0 > div:nth-child(2) > div > div > h3")
                            """).text,"You aren’t following anybody."))==True:
                                break
                        except:
                            pass