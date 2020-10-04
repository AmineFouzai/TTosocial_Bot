from selenium.webdriver import Chrome,ChromeOptions
from  selenium.webdriver.common.keys import Keys
from bs4 import  BeautifulSoup
from  halo import Halo
import sys
import time
from fastapi import FastAPI,Body,Response,Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app=FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

class Target(BaseModel):

	target_name:Optional[str]=None



@app.post('/api/scan')
async def scan(target: Target=Body(
	...,example={
				
				"target_name": "John constantine",
			}
))->Response:
			print(target.target_name)
			fbemail,fbpassword="98995823","python3kjkszpjassassing2"
			arg='--headless'
			SMM_Spinner=Halo(text='Initializing Facebook Module...',text_color='cyan',spinner='dots')   
			SMM_Spinner.start()
			options= ChromeOptions()
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
			SMM_Spinner.succeed(text='Facebook Page Initialized...')
			SMM_Spinner.succeed(text='Bot loged In... ')
			waitng_time=10
			try:
					time.sleep(waitng_time) 
					SMM_Spinner.text_color='cyan'
					SMM_Spinner.start('Initializing Facebook Search ... ')
					driver.execute_script("document.querySelector('[name=q]').value=''")
					driver.find_element_by_name('q').send_keys( target.target_name+Keys.RETURN)
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
					return {

						"facebook_based_search":users_urls,
						"Possible_Users":len(users_urls)

						}
			except Exception as e:
				raise e
			


# fbemail,fbpassword="98995823","python3kjkszpjassassing2"
# target="malek ben amo"
# arg=""#'--headless'
# SMM_Spinner=Halo(text='Initializing SMM Module...',text_color='cyan',spinner='dots')   
# SMM_Spinner.start()
# options=ChromeOptions()
# option=['--disable-notifications',arg] if arg !='' else ['--disable-notifications']
# [options.add_argument(opt) for opt in option]
# driver=Chrome(options=options)
# driver.get('https://www.facebook.com')
# domComplete = driver.execute_script("return window.performance.timing.domComplete - window.performance.timing.responseStart  ")
# waitng_time=domComplete/1000
# SMM_Spinner.info(f'FrontEnd Response Ended At: {domComplete/1000} second... ')
# SMM_Spinner.info('Trying To Establish Connection...')
# driver.find_element_by_id('email').send_keys(fbemail)
# driver.find_element_by_id('pass').send_keys(fbpassword+Keys.RETURN)        
# SMM_Spinner.text_color='green'
# SMM_Spinner.succeed(text='Connection Established...')
# SMM_Spinner.succeed(text='Social Media Module Initialized...')
# waitng_time=10
# try:
# 			time.sleep(waitng_time) 
# 			SMM_Spinner.text_color='cyan'
# 			SMM_Spinner.start('Initializing SubSMM Module... ')
# 			driver.execute_script("document.querySelector('[name=q]').value=''")
# 			driver.find_element_by_name('q').send_keys(target+Keys.RETURN)
# 			SMM_Spinner.text_color='blue'   
# 			SMM_Spinner.info('Quering For Results... ')

# 			time.sleep(waitng_time)
# 			try:
			
# 				users_data=driver.find_element_by_id('browse_result_area').get_attribute('innerHTML')
			
# 			except Exception as e:
# 				print(e)
# 				SMM_Spinner.text_color='yellow'
# 				SMM_Spinner.warn(' Dom Loading  Error...')
# 				driver.execute_script("document.querySelector('[name=q]').value=''")
# 				driver.find_element_by_name('q').send_keys(target+Keys.RETURN)
# 				SMM_Spinner.info(f'Correcting Error By Wating For Element Presence: {waitng_time} second...')
# 				time.sleep(waitng_time)
# 				users_data=driver.find_element_by_id('browse_result_area').get_attribute('innerHTML')
# 				SMM_Spinner.text_color='blue'

# 			users_urls=[a['href'] for a in BeautifulSoup(users_data,'html.parser').find_all('a',href=True,class_='_6xu6')]        
# 			SMM_Spinner.info(f'Possible Users Found [{len(users_urls)}]...')
# 			SMM_Spinner.info(f'Users URLS [{users_urls}]...') 

# except Exception as e:
# 	print(e)