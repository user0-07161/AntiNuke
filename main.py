import nextcord
from nextcord.ext import commands, application_checks
import json
from datetime import datetime
import threading
import time
import os
import pathlib
from dotenv import load_dotenv

everyonepingsinpast15secs = 0
restoring = 0
bot = commands.Bot(intents=nextcord.Intents.all())
raidtriggers = {

}
backups = {

}

try:
    with open('backups.json', 'r') as f:
        backups = json.load(f)
except:
    backups = {

    }
load_dotenv()

def everyoneraid():
    while True:
        time.sleep(3)
        global everyonepingsinpast15secs
        everyonepingsinpast15secs = 0
checkforeveryonepings = threading.Thread(name="Check for everyone pings every 15 seconds", target=everyoneraid)
checkforeveryonepings.start()

for trigger in os.listdir(pathlib.PurePath("src", "triggers")):
    fullpath = pathlib.PurePath("src", "triggers", trigger)
    if os.path.isfile(fullpath):
        with open(fullpath, "r", encoding="utf-8") as script:
            exec(script.read())
for command in os.listdir(pathlib.PurePath("src", "commands")):
    fullpath = pathlib.PurePath("src", "commands", command)
    if os.path.isfile(fullpath):
        with open(fullpath, "r", encoding="utf-8") as script:
            exec(script.read())

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Game(name=f"Protecting {str(len(bot.guilds))} servers"))
    print(f"Logged in as \"{bot.user}\"")
    
bot.run(os.getenv("TOKEN_DSC"))
    
    
