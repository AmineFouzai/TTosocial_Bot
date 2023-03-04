from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By


class LinkedinBot(Chrome):
   
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
        
        def run(self):
            self.connect()

        def connect(self):
            try:
                self.get(f"https://www.linkedin.com/login")
                self.find_element(by=By.ID,value="username").send_keys(self.login)
                self.find_element(by=By.ID,value="password").send_keys(self.password)
                self.execute_script("""document.querySelector('#organic-div > form > div.login__form_action_container > button').click()""")
            except Exception as e:
                print(e)
            else:
                    print("Connected !")
                    return True 