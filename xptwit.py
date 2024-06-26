import tweepy
import xphid

def sendtweet(tweettext,images):
    if len(images)>0:
        mediaids=[]
        for image in images:
            returnmedia=v1api.simple_upload(image)
            mediaids.append(returnmedia.media_id)
        postresponse=postclient.create_tweet(text=tweettext,user_auth=False,media_ids=mediaids)
    else:    
        postresponse=postclient.create_tweet(text=tweettext,user_auth=False)
    print('tweet sent')
    return(postresponse)

def startup():
    print(oauth2_user_handler.get_authorization_url())

    access_token=oauth2_user_handler.fetch_token(input("paste authorization response url: "))
    print("found access token: ",access_token)
    thisat=access_token['access_token']
    print('stored access token: ',thisat)
    thisrt=access_token['refresh_token']
    print('stored refresh token: ',thisrt)
    postclient=tweepy.Client(thisat, wait_on_rate_limit=True)
    return(thisat, thisrt, postclient)

def refreshcycle ():
    try:
        global thisrt
        global thisat
        global postclient
        print('refreshing token')
        newtokenresp=oauth2_user_handler.refresh_token('https://api.twitter.com/2/oauth2/token',refresh_token=thisrt)
        print('got token refresh response',newtokenresp)
        thisrt=newtokenresp['refresh_token']
        thisat=newtokenresp['access_token']
        print('stored access token: ',thisat)
        print('stored refresh token: ',thisrt)
        postclient=tweepy.Client(thisat, wait_on_rate_limit=True)
    except Exception as errortext:
        print('failed to process refreshcycle!!with error',errortext)

oauth2_user_handler=tweepy.OAuth2UserHandler(
    client_id=xphid.twitoa2clientid,
    redirect_uri=xphid.twitredirect_uri,
    scope=["tweet.read","tweet.write","users.read","offline.access"],
    client_secret=xphid.twitoa2clientsecret
    )

(thisat, thisrt, postclient)=startup()

v1auth=tweepy.OAuth1UserHandler(
    consumer_key=xphid.twitapikey,
    consumer_secret=xphid.twitapisecret,
    access_token=xphid.twitaccesstoken,
    access_token_secret=xphid.twitaccesssecret
)

v1api=tweepy.API(v1auth)

#schedule.every(90).minutes.do(refreshcycle)


#while True:
   # schedule.run_pending()
   # time.sleep(1)

