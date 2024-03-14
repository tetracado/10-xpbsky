import discord
import xphid
import xpbsky
import xptwit
from discord.ext import tasks
import os
import time
import re

mydir=os.path.dirname(__file__)
imgpath=os.path.join(mydir,'img')

@tasks.loop(minutes=90)
async def refreshtwitter():
    xptwit.refreshcycle()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    refreshtwitter.start()

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    try:
        print('message:',message)
        print('attachments',message.attachments)
        if  str(message.author)=="tetra6238" and "xpbot" in message.content.lower():       
            if len(message.content)>160:
                print('texts too long for tweet at',len(message.content),'rejected')     
                await message.channel.send('text too long for tweet at '+str(len(message.content))+' rejected')
            lines=message.content.splitlines()
            lines=lines[1:]
            tweettext='\n'.join(lines)
            print('got tweet request with lines',tweettext)
            savedpaths=[]
            if len(message.attachments)>0:
                print('downloading',len(message.attachments),'images')
                for attachment in message.attachments:
                    filetype='.'+re.findall('\/(.*)',attachment.content_type)[0]
                    print(filetype)
                    filename=os.path.join(imgpath,str(str(int(time.time())))+filetype)
                    savedpaths.append(filename)
                    time.sleep(1)
                    await attachment.save(filename)
                print('saved attachements')
            xpbsky.sendtweet(tweettext,savedpaths)
            xptwit.sendtweet(tweettext,savedpaths)
            await message.channel.send('bsky and tweet sent')

    except Exception as exception:
        print("error handled with exception",exception)
    
    await print('looping')

client.run(xphid.discbotkey)




