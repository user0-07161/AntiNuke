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
           
