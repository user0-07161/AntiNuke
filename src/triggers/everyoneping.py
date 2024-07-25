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