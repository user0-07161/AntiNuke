import nextcord
from nextcord.ext import commands, application_checks
import json
from datetime import datetime
import threading
import time
everyonepingsinpast15secs = 0
restoring = 0
bot = commands.Bot()
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
def everyoneraid():
    while True:
        time.sleep(3)
        global everyonepingsinpast15secs
        everyonepingsinpast15secs = 0
checkforeveryonepings = threading.Thread(name="Check for everyone pings every 15 seconds", target=everyoneraid)
checkforeveryonepings.start()
@bot.event
async def on_ready():
    print(f"Logged in as \"{bot.user}\"")
@bot.event
async def on_message(message):
    global everyonepingsinpast15secs
    global restoring
    channel = message.channel
    if message.mention_everyone:
        everyonepingsinpast15secs += 1
    if everyonepingsinpast15secs > 6 and restoring == 0:
        restoring = 1
        everyonepingsinpast15secs = 0
        try:
            everyonepingsinpast15secs = 0
            await message.author.kick(reason="Causing a possible raid")
            everyonepingsinpast15secs = 0
        except:
            everyonepingsinpast15secs = 0
            pass
        try:
            guildname = str(backups[str(message.guild.id)]["name"])
            await message.guild.edit(name=guildname)
        except:
            pass
        for channel in channel.guild.channels:
            try:
                everyonepingsinpast15secs = 0
                await channel.delete()
            except:
               everyonepingsinpast15secs = 0
               pass
        for category in channel.guild.categories:
            try:
                everyonepingsinpast15secs = 0
                await category.delete()
            except:
                everyonepingsinpast15secs = 0
                pass
        for role in channel.guild.roles:
            if not role.is_bot_managed() and not role.is_integration() and not role.is_default():
                try:
                    everyonepingsinpast15secs = 0
                    await role.delete()
                except:
                    everyonepingsinpast15secs = 0
                    pass
        try:
            for category in backups[str(channel.guild.id)]["categories"]:
                position = backups[str(channel.guild.id)]["categories"][str(category)]["position"]
                await channel.guild.create_category(str(category), reason="Restored", position=int(position))
        except:
            pass
        try:
            for textchannel in backups[str(channel.guild.id)]["textchannels"]:
                position = backups[str(channel.guild.id)]["textchannels"][str(textchannel)]["position"]
                try:
                    category = backups[str(channel.guild.id)]["textchannels"][str(textchannel)]["category"]
                except:
                    category = None
                    pass
                # Try to find category
                if category != None:
                    cgry = nextcord.utils.get(channel.guild.channels, name=category)
                try:
                    if cgry: 
                        await channel.guild.create_text_channel(str(textchannel), reason="Restored", category=cgry, position=int(position))
                    else:
                        await channel.guild.create_text_channel(str(textchannel), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await channel.guild.create_text_channel(str(textchannel), reason="Restored", position=int(position))
        except:
            pass
        try:
            for voicechannel in backups[str(channel.guild.id)]["voicechannels"]:
                try:
                    category = backups[str(channel.guild.id)]["voicechannels"][str(voicechannel)]["category"]
                except:
                    category = None
                    pass
                position = backups[str(channel.guild.id)]["voicechannels"][str(voicechannel)]["position"]
                if category != None:
                    cgry = nextcord.utils.get(channel.guild.channels, name=category)
                try:
                    if cgry: 
                        await channel.guild.create_voice_channel(str(voicechannel), reason="Restored", category=cgry, position=int(position))
                    else:
                        await channel.guild.create_voice_channel(str(voicechannel), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await channel.guild.create_voice_channel(str(voicechannel), reason="Restored", position=int(position))
        except:
            pass
        try:
            for thread in backups[str(channel.guild.id)]["thread"]:
                try:
                    category = backups[str(channel.guild.id)]["thread"][str(thread)]["category"]
                except:
                    category = None
                    pass
                position = backups[str(channel.guild.id)]["thread"][str(thread)]["position"]
                if category != None:
                    cgry = nextcord.utils.get(channel.guild.channels, name=category)
                try:
                    if cgry: 
                        await channel.guild.create_forum_channel(str(thread), reason="Restored", category=cgry, position=int(position))
                    else:
                        await channel.guild.create_forum_channel(str(thread), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await channel.guild.create_forum_channel(str(thread), reason="Restored", position=int(position))
        except:
            pass
        try:
            for stage in backups[str(channel.guild.id)]["stages"]:
                try:
                    category = backups[str(channel.guild.id)]["stages"][str(stage)]["category"]
                except:
                    category = None
                    pass
                position = backups[str(channel.guild.id)]["stages"][str(stage)]["position"]
                if category != None:
                    cgry = nextcord.utils.get(channel.guild.channels, name=category)
                try:
                    if cgry: 
                        await channel.guild.create_forum_channel(str(stage), reason="Restored", category=cgry, position=int(position))
                    else:
                        await channel.guild.create_forum_channel(str(stage), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await channel.guild.create_forum_channel(str(stage), reason="Restored", position=int(position))
            for role in backups[str(channel.guild.id)]["roles"]:
                perms = nextcord.Permissions(backups[str(channel.guild.id)]["roles"][str(role)]["permissions"])
                await channel.guild.create_role(name=str(role), permissions=perms)
        except:
            pass
        everyonepingsinpast15secs = 0
        restoring = 0
@bot.slash_command(description="Create a backup for this server")
@application_checks.has_permissions(manage_messages=True)    
async def createbackup(interaction: nextcord.Interaction):
    roles = []
    channels = []
    categories = []
    try:
        if not backups[str(interaction.guild.id)]:
            backups[str(interaction.guild.id)] = {}
    except:
        backups[str(interaction.guild.id)] = {}
    backups[str(interaction.guild.id)]["textchannels"] = {}
    backups[str(interaction.guild.id)]["categories"] = {}
    backups[str(interaction.guild.id)]["voicechannels"] = {}
    backups[str(interaction.guild.id)]["threads"] = {}
    backups[str(interaction.guild.id)]["stages"] = {}
    backups[str(interaction.guild.id)]["roles"] = {}
    backups[str(interaction.guild.id)]["name"] = interaction.guild.name
    for textchannel in interaction.guild.text_channels:
        backups[str(interaction.guild.id)]["textchannels"][textchannel.name] = {}
        backups[str(interaction.guild.id)]["textchannels"][textchannel.name]["position"] = textchannel.position
        try:
            backups[str(interaction.guild.id)]["textchannels"][textchannel.name]["category"] = textchannel.category.name
        except:
            backups[str(interaction.guild.id)]["textchannels"][textchannel.name]["category"] = None
        channels.append(textchannel.name)
    for category in interaction.guild.categories:
        backups[str(interaction.guild.id)]["categories"][category.name] = {}
        backups[str(interaction.guild.id)]["categories"][category.name]["position"] = category.position
        categories.append(category.name)
    for voicechannel in interaction.guild.voice_channels:
        backups[str(interaction.guild.id)]["voicechannels"][voicechannel.name] = {}
        backups[str(interaction.guild.id)]["voicechannels"][voicechannel.name]["position"] = voicechannel.position
        try:
            backups[str(interaction.guild.id)]["voicechannels"][voicechannel.name]["category"] = voicechannel.category.name
        except:
            pass
        channels.append(voicechannel.name)
    for thread in interaction.guild.forum_channels:
        backups[str(interaction.guild.id)]["threads"][thread.name] = {}
        backups[str(interaction.guild.id)]["threads"][thread.name]["position"] = 1
        try:
            backups[str(interaction.guild.id)]["threads"][thread.name]["category"] = thread.category.name
        except:
            pass
        channels.append(thread.name)
    for stage in interaction.guild.stage_channels:
        backups[str(interaction.guild.id)]["stages"][stage.name] = {}
        backups[str(interaction.guild.id)]["stages"][stage.name]["position"] = stage.position
        try:
            backups[str(interaction.guild.id)]["stages"][stage.name]["category"] = stage.category.name
        except:
            pass
    for role in interaction.guild.roles:
        if not role.is_bot_managed() and not role.is_integration() and not role.is_default():
            backups[str(interaction.guild.id)]["roles"][role.name] = {}
            backups[str(interaction.guild.id)]["roles"][role.name]["position"] = role.position
            backups[str(interaction.guild.id)]["roles"][role.name]["permissions"] = int(role.permissions.value)
        roles.append(role.name)
    with open("backups.json", "w") as f:
        json.dump(backups, f)
    embed = nextcord.Embed(title=f"Backup successfully created (Server name: \'{interaction.guild.name}\')", description="Your server is prepared for raids now :smiling_imp:\nHere's what I backed up:")
    embed.add_field(name=f"{len(roles)} Roles", value=f"{', '.join(roles)}")
    embed.add_field(name=f"{len(channels)} Channels, Threads and VCs", value=f"{', '.join(channels)}")
    embed.add_field(name=f"{len(categories)} Categories", value=f"{', '.join(categories)}")
    await interaction.send(embed=embed)
@bot.slash_command(description="Get informations about the current backup")
async def backupinfo(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="Fetching informations...", description="Please wait!")
    msg = await interaction.send(embed=embed)
    channels = []
    categories = []
    roles = []
    for channel in backups[str(interaction.guild.id)]["textchannels"]:
        channels.append(channel)
    for channel in backups[str(interaction.guild.id)]["voicechannels"]:
        channels.append(channel)
    for channel in backups[str(interaction.guild.id)]["threads"]:
        channels.append(channel)
    for channel in backups[str(interaction.guild.id)]["stages"]:
        channels.append(channel)
    for category in backups[str(interaction.guild.id)]["categories"]:
        categories.append(category)
    for role in backups[str(interaction.guild.id)]["roles"]:
        roles.append(role)
    embed = nextcord.Embed(title=interaction.guild.name, description="The latest backup contans...")
    embed.add_field(name=f"{len(roles)} roles", value=f"{', '.join(roles)}")
    embed.add_field(name=f"{len(channels)} channels, voice channels, stages and forums", value=f"{', '.join(channels)}")
    embed.add_field(name=f"{len(categories)} categories", value=f"{', '.join(categories)}")
    await msg.edit(embed=embed)

@bot.slash_command(description="Manually load the latest available backup (owner only)")
async def loadbackup(interaction: nextcord.Interaction):
    if interaction.guild.owner_id == interaction.user.id:
        guildname = str(backups[str(interaction.guild.id)]["name"])
        await interaction.guild.edit(name=guildname)
        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except:
                pass
        for category in interaction.guild.categories:
            try:
                await category.delete()
            except:
                pass
        for role in interaction.guild.roles:
            if not role.is_bot_managed() and not role.is_integration() and not role.is_default():
                try:
                    await role.delete()
                except:
                    pass
        try:
            for category in backups[str(interaction.guild.id)]["categories"]:
                position = backups[str(interaction.guild.id)]["categories"][str(category)]["position"]
                await interaction.guild.create_category(str(category), reason="Restored", position=int(position))
        except:
            pass
        try:
            for textchannel in backups[str(interaction.guild.id)]["textchannels"]:
                position = backups[str(interaction.guild.id)]["textchannels"][str(textchannel)]["position"]
                category = backups[str(interaction.guild.id)]["textchannels"][str(textchannel)]["category"]
                # Try to find category
                if category != None:
                    cgry = nextcord.utils.get(interaction.guild.channels, name=category)
                try:
                    if cgry: 
                        await interaction.guild.create_text_channel(str(textchannel), reason="Restored", category=cgry, position=int(position))
                    else:
                        await interaction.guild.create_text_channel(str(textchannel), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await interaction.guild.create_text_channel(str(textchannel), reason="Restored", position=int(position))
        except:
            pass
        try:
            for voicechannel in backups[str(interaction.guild.id)]["voicechannels"]:
                category = backups[str(interaction.guild.id)]["voicechannels"][str(voicechannel)]["category"]
                position = backups[str(interaction.guild.id)]["voicechannels"][str(voicechannel)]["position"]
                if category != None:
                    cgry = nextcord.utils.get(interaction.guild.channels, name=category)
                try:
                    if cgry: 
                        await interaction.guild.create_voice_channel(str(voicechannel), reason="Restored", category=cgry, position=int(position))
                    else:
                        await interaction.guild.create_voice_channel(str(voicechannel), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await interaction.guild.create_voice_channel(str(voicechannel), reason="Restored", position=int(position))
        except:
            pass
        try:
            for thread in backups[str(interaction.guild.id)]["thread"]:
                category = backups[str(interaction.guild.id)]["thread"][str(thread)]["category"]
                position = backups[str(interaction.guild.id)]["thread"][str(thread)]["position"]
                if category != None:
                    cgry = nextcord.utils.get(interaction.guild.channels, name=category)
                try:
                    if cgry: 
                        await interaction.guild.create_forum_channel(str(thread), reason="Restored", category=cgry, position=int(position))
                    else:
                        await interaction.guild.create_forum_channel(str(thread), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await interaction.guild.create_forum_channel(str(thread), reason="Restored", position=int(position))
        except:
            pass
        try:
            for stage in backups[str(interaction.guild.id)]["stages"]:
                category = backups[str(interaction.guild.id)]["stages"][str(stage)]["category"]
                position = backups[str(interaction.guild.id)]["stages"][str(stage)]["position"]
                if category != None:
                    cgry = nextcord.utils.get(interaction.guild.channels, name=category)
                try:
                    if cgry: 
                        await interaction.guild.create_forum_channel(str(stage), reason="Restored", category=cgry, position=int(position))
                    else:
                        await interaction.guild.create_forum_channel(str(stage), reason="Restored", position=int(position))
                except Exception as e:
                    print(e)
                    await interaction.guild.create_forum_channel(str(stage), reason="Restored", position=int(position))
            for role in backups[str(interaction.guild.id)]["roles"]:
                perms = nextcord.Permissions(backups[str(interaction.guild.id)]["roles"][str(role)]["permissions"])
                await interaction.guild.create_role(name=str(role), permissions=perms)
        except:
            pass
    else:
        embed = nextcord.Embed(title="No permissions", description="Only the server owner is able to do that.")
        await interaction.send(embed=embed)
           

        
    
bot.run("Place your token here, enable all intents.")
    
    