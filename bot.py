# bot.py
import os
import random
from datetime import datetime

from dl import *

import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.all()
intents.members = True
client = discord.Client(intents=intents)


@client.event
async def on_ready():

    for guild in client.guilds:
        if guild.name == GUILD:
            break
    # guild = discord.utils.find(lambda g:g.name == GUILD, client.guilds)
    # guild = discord.utils.get(client.guilds, name=GUILD)
    
    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'  
    )
    members = '\n - '.join([member.name for member in guild.members])
    print(f'Guild Members:\n - {members}')


# Welcome new user to server.
@client.event
async def on_member_join(member):
    await member.create_dm_()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord Server!'
    )

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    command = message.content[1:].split(' ')
    print(command)

    if command[0] == ('ping'):
        response = ((datetime.now() - message.created_at).seconds / 100)
        await message.channel.send(f'Pong! Message Reponse Time = {response}ms')
    '''
    if command[0] == 'framedata':
        response = findNormalData('5P')
        await message.channel.send('```'+ response + '```')
    '''

    '''
    if command[0] == 'systemdata':
    '''

    # Guilty Gear Strive specific frame data
    # Maybe have the embed in a different file.
    if command[0] =='framedata':

        ##### To be added when other games have consistent tables. #####
        #game = command[1].lower()
        #character = command[2].lower()
        #move = command[3].upper()

        character = command[1].lower()
        move = command[2].upper()

        embed=discord.Embed(title=f'{striveCharacters[character]} {move}', url=f'https://dustloop.com/wiki/index.php?title=GGST/{striveCharacters[character]}#{move}', color=0xFF5733)
        # Have footer tell user about [] notation from dustloop, special case for certain characters.
        embed.set_footer(text='balls')
        frameData = findStriveFrameData(striveCharacters[character],move)

        # Some moves have no name, such as reflect projectile, perhaps just omit this if that's the case.
        # If url provides an error, probably skip.
        embed.set_thumbnail(url = moveStriveImage(striveCharacters[command[1].lower()], move))

        
        # There are empty strings in the frame data sent and embed doesn't like that.
        i = 0
        for data in frameData[0]:
            embed.add_field(name=f'{frameData[0][i]}', value=f'{frameData[1][i]}', inline='True')
            i+=1
        
        await message.channel.send(embed=embed)



client.run(TOKEN)