import xpsel
import xphid
from selenium import webdriver
import platform
#from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import re
from atproto import Client, models
import schedule

def readtweets(link):
    try:
        xpsel.openlink(link)

        #check for new tweets

        alltweets=xpsel.driver.find_elements(By.CLASS_NAME, "timeline-item")
        print ('found', (len(alltweets)), 'tweets')
        for tweet in alltweets:
            print('testing',tweet)
            try:
                print(tweet.find_element(By.CLASS_NAME,"tweet-link").get_attribute("href"))
                if dupecheck(tweet.find_element(By.CLASS_NAME,"tweet-link").get_attribute("href"))==True:
                    print('found old tweet, skipping')
                else:
                    print('found unique tweet')   
                    try:
                        rtcheck=tweet.find_element(By.CLASS_NAME,"retweet-header")
                        rtacc=tweet.find_element(By.CLASS_NAME,"username").get_attribute("title")
                        print('retweet identified from',rtacc)
                    except NoSuchElementException:
                        try:
                            imgtweet=tweet.find_element(By.CLASS_NAME,"attachments")
                            print('attachment tweet identified from my account')
                            try:
                                stillimages=imgtweet.find_elements(By.CLASS_NAME,"still-image")
                                mediatext=tweet.find_element(By.CLASS_NAME,"tweet-content").text
                                print('found mediatext tweet from my account:',mediatext,'posting now')
                                maybethiswilluploadimages(extractimages(stillimages),mediatext)
                            except:
                                print('couldnt extract images')
                        except NoSuchElementException:
                            try:
                                plaintext=tweet.find_element(By.CLASS_NAME,"tweet-content").text
                                print('found plaintext tweet from my account:',plaintext,'posting now')
                                bskyclient.send_post(text=plaintext)
                            except NoSuchElementException:
                                print('couldnt process tweet like at all')
            except NoSuchElementException:
                print('couldnt find tweet link, skipping')
                continue
    except Exception as errortext:
         print('failed to read all tweets with error:',errortext)
         
def extractimages(stillimages):
    imgpaths=[]
    for image in stillimages:
        imglink=image.get_attribute("href")
        print('got imglink:',imglink)
        newpath=xpsel.saveimg(imglink)
        print('got saved image path',newpath)
        imgpaths.append(newpath)
    return imgpaths

def maybethiswilluploadimages(imagepaths,textpost):
    allimages=[]
    for imagepath in imagepaths:
        with open(imagepath, 'rb') as file:
            img_data=file.read()
            upload=bskyclient.com.atproto.repo.upload_blob(img_data)
            allimages.append(models.AppBskyEmbedImages.Image(alt='no alt text available', image=upload.blob))
    embed = models.AppBskyEmbedImages.Main(images=allimages)
    bskyclient.com.atproto.repo.create_record(
        models.ComAtprotoRepoCreateRecord.Data(
            repo=bskyclient.me.did,
            collection=models.ids.AppBskyFeedPost,
            record=models.AppBskyFeedPost.Main(
                created_at=bskyclient.get_current_time_iso(), text=textpost, embed=embed
            ),
        )
    )


    




def dupecheck(link):
    try:
        fhand=open('usedlinks.txt','r+')
        print('opened usedlinks.txt')
        found=False
        for line in fhand:
            if link in line:
                print('EXITING!! found testlink:',link)
                found=True
                fhand.close()
                print('retained and closed usedlinks.txt')
                return(True)
                break
        if found==False:
            print('adding new link:',link)
            #xpsel.openlink(link)
            fhand.write(link+'\n')
            fhand.close()
            print('wrote and closed usedlinks.txt')
            return(False)
    except:
        print('couldnt find link')
        found=False

bskyclient=Client()
bskyclient.login('tetracado.bsky.social', xphid.bskyapppass)
print('logged in to bsky')

#readtweets("https://nitter.net/tetracado")


schedule.every(1).hour.do(readtweets,"https://nitter.net/tetracado") 

while True:
    schedule.run_pending()
    time.sleep(1)