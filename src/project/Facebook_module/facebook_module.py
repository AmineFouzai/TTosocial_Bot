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
fbemail,fbpassword=sys.argv[1],sys.argv[2]
target="target"
path="target.jpg"
arg=""#'--headless'
SMM_Spinner=Halo(text='Initializing SMM Module...',text_color='cyan',spinner='dots')   
SMM_Spinner.start()
options=ChromeOptions()
option=['--disable-notifications',arg] if arg !='' else ['--disable-notifications']
[options.add_argument(opt) for opt in option]
driver=Chrome(options=options)
driver.get('https://www.facebook.com')
domComplete = driver.execute_script("return window.performance.timing.domComplete - window.performance.timing.responseStart  ")
waitng_time=domComplete/1000
SMM_Spinner.info(f'FrontEnd Response Ended At: {domComplete/1000} second... ')
SMM_Spinner.info('Trying To Establish Connection...')
driver.find_element_by_id('email').send_keys(fbemail)
driver.find_element_by_id('pass').send_keys(fbpassword+Keys.RETURN)        
SMM_Spinner.text_color='green'
SMM_Spinner.succeed(text='Connection Established...')
SMM_Spinner.succeed(text='Social Media Module Initialized...')
waitng_time=10
try:
			time.sleep(waitng_time) 
			SMM_Spinner.text_color='cyan'
			SMM_Spinner.start('Initializing SubSMM Module... ')
			driver.execute_script("document.querySelector('[name=q]').value=''")
			driver.find_element_by_name('q').send_keys(target+Keys.RETURN)
			SMM_Spinner.text_color='blue'   
			SMM_Spinner.info('Quering For Results... ')

			time.sleep(waitng_time)
			try:
			
				users_data=driver.find_element_by_id('browse_result_area').get_attribute('innerHTML')
			
			except Exception as e:
				print(e)
				SMM_Spinner.text_color='yellow'
				SMM_Spinner.warn(' Dom Loading  Error...')
				driver.execute_script("document.querySelector('[name=q]').value=''")
				driver.find_element_by_name('q').send_keys(target+Keys.RETURN)
				SMM_Spinner.info(f'Correcting Error By Wating For Element Presence: {waitng_time} second...')
				time.sleep(waitng_time)
				users_data=driver.find_element_by_id('browse_result_area').get_attribute('innerHTML')
				SMM_Spinner.text_color='blue'
			
			users_urls=[a['href'] for a in BeautifulSoup(users_data,'html.parser').find_all('a',href=True,class_='_6xu6')]        
			SMM_Spinner.info(f'Possible Users Found [{len(users_urls)}]...')
			SMM_Spinner.info(f'Users URLS [{users_urls}]...') 
			for key,value in enumerate(users_urls):
				SMM_Spinner.info(f'Looking For User With Url [{value}]...')
				try:
					driver.get(value)
				except Exception:
					SMM_Spinner.text_color='yellow'
					SMM_Spinner.warn('Bad Formated URl Has Been Found...')
					SMM_Spinner.text_color='yellow'
					SMM_Spinner.info('correcting URL...')
					value='https://www.facebook.com'+value
					driver.get(value)
	
				SMM_Spinner.text_color='green'
				SMM_Spinner.succeed('Url testing Passd...')
				time.sleep(waitng_time)
				user_profile=driver.find_element_by_css_selector('img._11kf.img').click() 
				SMM_Spinner.text_color='cyan'
				SMM_Spinner.succeed('Saving Profile Picture...!')
				time.sleep(waitng_time)
				driver.save_screenshot(f'user{key}.png')#adjust path
				SMM_Spinner.text_color='cyan'
				SMM_Spinner.start('Initializing Recognizer Module... ')
				simple_compare_result=Simple_Faces_Compare(path,f'user{key}.png')
				if(isinstance(simple_compare_result,bool)):   
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
						driver.get(value+'?sk=photos')
						driver.execute_script("document.querySelector('#pagelet_timeline_medley_photos').scrollIntoView()")
					except Exception :
						driver.get(value+'&sk=photos')
						driver.execute_script("document.querySelector('#pagelet_timeline_medley_photos').scrollIntoView()")
					driver.find_element_by_id('pagelet_timeline_medley_photos').screenshot(f'user_face{key}.png')
					forced_compare_result=Foreced_Faces_Compare(f'user_face{key}.png',path)
					if(isinstance(forced_compare_result,bool)):
						SMM_Spinner.text_color='green'
						SMM_Spinner.succeed(f'Match 100% ,Result[{forced_compare_result}]')
						SMM_Spinner.succeed('Forced Comparing Module Termenated ... [status OK!]')
						SMM_Spinner.succeed('Target Found Rolling back in Memeory... ')
						break
				# return value+'/about'
					else:
						SMM_Spinner.text_color='red'
						SMM_Spinner.warn('Forced Comparing Module Faild...! ')
						SMM_Spinner.text_color='blue'
						SMM_Spinner.info('Passing To The Next User Scan...')
						continue
				else:continue
			SMM_Spinner.stop()
except Exception as e:
		   raise e 
		   SMM_Spinner.text_color='red' 
		   SMM_Spinner.fail('Connection TimeOut !!!')
		   SMM_Spinner.fail('Fatal Error !!!')
		   SMM_Spinner.fail('Unhandeled URL Accured !!!')
		   SMM_Spinner.fail('Weak input Provided Error !!!')
		   SMM_Spinner.fail(' Check Target Potinelle Profile Name!!!')
		   driver.close()
		   exit()

