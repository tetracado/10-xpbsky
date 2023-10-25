from selenium import webdriver
import platform
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
#from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
import os
import xphid
import requests

mydir=os.path.dirname(__file__)

options=Options()
#options.BinaryLocation='/usr/bin/chromium-browser'
options.add_argument('--disable-infobars')
options.add_argument('--disable-extensions')
options.add_argument('--disable-gpu')
#options.add_argument('--headless')
options.add_argument('--window-size=1024,1068')
#driver_path='/usr/bin/chromedriver'
#service=ChromeService()

driver = webdriver.Chrome(options=options)#,service=service)

def openlink(link):
    print('opening:',link)
    driver.get(link)
    time.sleep(5)

def saveimg(link):
    print('opening',link)
    filetype=re.findall("\S*([.].*)",link)[0]
    imgname=str(str(int(time.time())))+filetype
    imgpath=os.path.join(mydir,'img',imgname)
    print('about to save img at:',imgpath)
    img_data=requests.get(link,headers={'User-Agent': 'ABC/3.0'}).content
    savefile= open(imgpath,'wb')
    savefile.write(img_data)
    savefile.close()
    print('returning image path',imgpath)
    return(imgpath)


#saveimg("https://nitter.net/pic/orig/media%2FF9QF2SRasAAzY7B.png")
#saveimg("https://media.geeksforgeeks.org/wp-content/uploads/20210224040124/JSBinCollaborativeJavaScriptDebugging6-300x160.png")