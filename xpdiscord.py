# This example requires the 'message_content' intent.
import discord
import xphid
import xpbsky
import xptwit
from discord.ext import tasks

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
        print(message)
        if  str(message.author)=="tetra6238" and "xpbot" in message.content.lower():       
            if len(message.content)>160:
                print('text too long for tweet at',len(message.content),'rejected')     
            lines=message.content.splitlines()
            lines=lines[1:]
            tweettext='\n'.join(lines)
            print('got tweet request with lines',tweettext)
            xpbsky.sendtweet(tweettext)
            xptwit.sendtweet(tweettext)

    except Exception as exception:
        print("error handled with exception",exception)
    
    await print('looping')

client.run(xphid.discbotkey)




