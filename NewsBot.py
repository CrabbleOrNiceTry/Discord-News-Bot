import sys
import asyncio
import discord
from bs4 import BeautifulSoup as bs4
import requests
import random
import datetime
import time
from discord.ext import tasks


client = discord.Client()
timeSinceLastUpdate = 0.0

async def GetWebPage():
    rand = random.randint(1, 8)
    switcher = {
        1: "https://news.google.com/topics/CAAqIggKIhxDQkFTRHdvSkwyMHZNRGxqTjNjd0VnSmxiaWdBUAE?hl=en-US&gl=US&ceid=US%3Aen", # U.S
        2: "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", # World
        3: "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx6TVdZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", # Business
        4: "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGRqTVhZU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", # Technology
        5: "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNREpxYW5RU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", # Entertainment
        6: "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp1ZEdvU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", # Sports
        7: "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRFp0Y1RjU0FtVnVHZ0pWVXlnQVAB?hl=en-US&gl=US&ceid=US%3Aen", # Science
        8: "https://news.google.com/topics/CAAqIQgKIhtDQkFTRGdvSUwyMHZNR3QwTlRFU0FtVnVLQUFQAQ?hl=en-US&gl=US&ceid=US%3Aen", # Health
    }
    return switcher.get(rand, "Something went wrong")

async def getNews():
    f = open('news.txt', 'a')
    page = requests.get(await GetWebPage())
    if (page.status_code != 200):
        raise Exception("error page not downloaded propperly.")
    soup = bs4(page.content, 'html.parser')
    elements = soup.find_all(class_="DY5T1d RZIKme")
    text_href = [[]]
    for i in elements:
        text_href.append([i.text, i['href']])
    rand = random.randint(1, 5)

    # Get one of the top 5 articles this list contains title, link
    selected_article = text_href[rand]
    selected_article_link = "https://news.google.com/"
    selected_article_link += selected_article[1][2:]
    
    # Prints the article title, link
    print(selected_article)

    # Get the redirected url which is the main source
    response = requests.get(selected_article_link)
    print(response.url)
    
    x = datetime.datetime.now()

    f.write(selected_article[0] + '\n' + response.url + '\n' + x.strftime("%c") + '\n--------------------\n')
    f.close()
    await asyncio.sleep(86400)
    await getNews()

@tasks.loop(seconds=0.2)
async def startNewsTimes():
    global timeSinceLastUpdate 
    timeSinceLastUpdate += 0.2
    x = datetime.datetime.now()
    if (x.strftime("%a") == 'Fri' and x.strftime("%H") == '12' and x.strftime("%M") == '30' and x.strftime("%S") == '30' and timeSinceLastUpdate > 2.0):
        timeSinceLastUpdate = 0
        channel = client.get_channel('Channel ID goes here, except this would be an int not a str')
        message = ""
        f = open('news.txt', 'r')
        for i in f:
            message += i
        await channel.send(message)




@client.event
async def on_ready():
    print ("Discord bot up and running")
    f = open('news.txt', 'w')

    f.write('++++++++++++++++++++\n')
    f.close() 
    startNewsTimes.start()
    await getNews()




client.run('Secret key goes here!')
