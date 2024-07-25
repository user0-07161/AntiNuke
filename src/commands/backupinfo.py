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
