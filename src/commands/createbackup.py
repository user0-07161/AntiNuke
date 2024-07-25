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