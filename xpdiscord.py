import discord
import xphid
import xpbsky
import xptwit
from discord.ext import tasks
import os
import time
import re
from PIL import Image

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

def reducefilesizes(savedpaths):
    for path in savedpaths:
        filesize=os.path.getsize(path)
        while filesize>1000000:
            print('image file size too big at',filesize)
            im=Image.open(path)
            im=im.resize((im.width//2,im.height//2))
            im.save(path,quality=75,optimize=True)
            filesize=os.path.getsize(path)
            print('saved image with reduced file size',filesize)


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    try:
        print('message:',message)
        print('attachments',message.attachments)
        if  str(message.author)=="tetra6238" and "xpbot" in message.content.lower():       
            if len(message.content)>260:
                print('texts too long for tweet at',len(message.content),'rejected')     
                await message.channel.send('text too long for tweet at '+str(len(message.content))+' rejected')
                return
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
                reducefilesizes(savedpaths)
            xpbsky.sendtweet(tweettext,savedpaths)
            await message.channel.send('bsky sent')
            xptwit.sendtweet(tweettext,savedpaths)
            await message.channel.send('tweet sent')
            return

    except Exception as exception:
        print("error handled with exception",exception)
        await message.channel.send('error handled with exception '+str(exception))

client.run(xphid.discbotkey)




