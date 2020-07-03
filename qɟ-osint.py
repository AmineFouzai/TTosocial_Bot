from selenium.webdriver import Chrome,ChromeOptions
from  selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from recognizer import Simple_Faces_Compare,Foreced_Faces_Compare
from bs4 import  BeautifulSoup
from json import JSONDecoder
from  halo import Halo
import sys
import time
SMM_Spinner=Halo(text='Initializing SMM Module...',text_color='cyan',spinner='dots')
       
class Social_Meadia_Module(Chrome):
    
    def __init__(self,FBemail,FBpassword,arg):    
        SMM_Spinner.start()
        options=ChromeOptions()
        option=['--disable-notifications',arg] if arg !='' else ['--disable-notifications']
        [options.add_argument(opt) for opt in option]
        super().__init__(options=options)
        self.get('https://www.facebook.com')
        domComplete = self.execute_script("return window.performance.timing.domComplete - window.performance.timing.responseStart  ")
        self.waitng_time=domComplete/1000
        SMM_Spinner.info(f'FrontEnd Response Ended At: {domComplete/1000} second... ')
        SMM_Spinner.info('Trying To Establish Connection...')
        self.find_element_by_id('email').send_keys(FBemail)
        self.find_element_by_id('pass').send_keys(FBpassword+Keys.RETURN)        
        SMM_Spinner.text_color='green'
        SMM_Spinner.succeed(text='Connection Established...')
        SMM_Spinner.succeed(text='Social Media Module Initialized...')
    
    def Profile(self,target,path):
        try:
            time.sleep(self.waitng_time) 
            SMM_Spinner.text_color='cyan'
            SMM_Spinner.start('Initializing SubSMM Module... ')
            self.execute_script("document.querySelector('[name=q]').value=''")
            self.find_element_by_name('q').send_keys(target+Keys.RETURN)
            SMM_Spinner.text_color='blue'   
            SMM_Spinner.info('Quering For Results... ')
            domComplete = self.execute_script("return window.performance.timing.domComplete - window.performance.timing.responseStart  ")
            self.waitng_time=domComplete/1000
            SMM_Spinner.info('Wating For Dom to Complete Done...')
            SMM_Spinner.info(f'FrontEnd Response Ended At: {domComplete/1000} second...')
            time.sleep(self.waitng_time)
            try:
            
                users_data=self.find_element_by_id('browse_result_area').get_attribute('innerHTML')
            
            except Exception:
                SMM_Spinner.text_color='yellow'
                SMM_Spinner.warn(' Dom Loading  Error...')
                self.execute_script("document.querySelector('[name=q]').value=''")
                self.find_element_by_name('q').send_keys(target+Keys.RETURN)
                SMM_Spinner.info(f'Correcting Error By Wating For Element Presence: {domComplete/1000} second...')
                time.sleep(self.waitng_time)
                users_data=self.find_element_by_id('browse_result_area').get_attribute('innerHTML')
                SMM_Spinner.text_color='blue'
            
            users_urls=[a['href'] for a in BeautifulSoup(users_data,'html.parser').find_all('a',href=True,class_='_6xu6')]        
            SMM_Spinner.info(f'Possible Users Found [{len(users_urls)}]...')
            SMM_Spinner.info(f'Users URLS [{users_urls}]...') 
            for key,value in enumerate(users_urls):
                SMM_Spinner.info(f'Looking For User With Url [{value}]...')
                try:
                    self.get(value)
                except Exception:
                    SMM_Spinner.text_color='yellow'
                    SMM_Spinner.warn('Bad Formated URl Has Been Found...')
                    SMM_Spinner.text_color='yellow'
                    SMM_Spinner.info('correcting URL...')
                    value='https://www.facebook.com'+value
                    self.get(value)
    
                SMM_Spinner.text_color='green'
                SMM_Spinner.succeed('Url testing Passd...')
                time.sleep(self.waitng_time)
                user_profile=self.find_element_by_css_selector('img._11kf.img').click() 
                SMM_Spinner.text_color='cyan'
                SMM_Spinner.succeed('Saving Profile Picture...!')
                time.sleep(self.waitng_time)
                self.save_screenshot(f'user{key}.png')#adjust path
                SMM_Spinner.text_color='cyan'
                SMM_Spinner.start('Initializing Recognizer Module... ')
                simple_compare_result=Simple_Faces_Compare(path,f'user{key}.png')
                if(simple_compare_result):   
                    SMM_Spinner.text_color='green'
                    SMM_Spinner.succeed(f'Match 100% ,Result [{simple_compare_result}]... ')
                    SMM_Spinner.text_color='green'
                    SMM_Spinner.succeed('Target Found Rolling back in Memeory... ')
                    break
                # return value+'/about'
                elif not simple_compare_result:
                    SMM_Spinner.text_color='red'
                    SMM_Spinner.warn('Simple Comparing Module Faild...! ')
                    SMM_Spinner.text_color='blue'
                    SMM_Spinner.info('Passing To The Next Forced Faces Scan...')
                    try:
                        self.get(value+'?sk=photos')
                        self.execute_script("document.querySelector('#pagelet_timeline_medley_photos').scrollIntoView()")
                    except Exception :
                        self.get(value+'&sk=photos')
                        self.execute_script("document.querySelector('#pagelet_timeline_medley_photos').scrollIntoView()")
                    self.find_element_by_id('pagelet_timeline_medley_photos').screenshot(f'user_face{key}.png')
                    forced_compare_result=Foreced_Faces_Compare(f'user_face{key}.png',path)
                    if(forced_compare_result):
                        SMM_Spinner.text_color='green'
                        SMM_Spinner.succeed(f'Match 100% ,Result[{forced_compare_result}]')
                        SMM_Spinner.succeed('Forced Comparing Module Termenated ... [status OK!]')
                        SMM_Spinner.succeed('Target Found Rolling back in Memeory... ')
                        break
                # return value+'/about'
                    else:continue
                else:continue
            SMM_Spinner.stop()
        except Exception:
           SMM_Spinner.text_color='red' 
           SMM_Spinner.fail('Connection TimeOut !!!')
           SMM_Spinner.fail('Fatal Error !!!')
           SMM_Spinner.fail('Unhandeled URL Accured !!!')
           SMM_Spinner.fail('Weak input Provided Error !!!')
           SMM_Spinner.fail(' Check Target Potinelle Profile Name!!!')
           self.close()
           exit()

#'--headless'
SMM=Social_Meadia_Module(sys.argv[1],sys.argv[2] ,sys.argv[3] if sys.argv[3]!=None else '' )
json=JSONDecoder()
data=dict(json.decode((open('targets.json','r').read())))
for key in data['brute_force']:     
        SMM.Profile(key,data['brute_force'][key])
SMM.close()
SMM.Profile('Skander Hammami','images_db/hazem.jpg')