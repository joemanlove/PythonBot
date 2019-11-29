# settings should have prefix and token variables
from settings import *
# get audio utilities specifically
from discord import FFmpegPCMAudio, PCMVolumeTransformer

import os
from random import choice

# import discord python library
import discord
# import the command module
from discord.ext import commands

# set the filepath for the audio decoder
ffmpeg_path = ffmpeg_path = 'ffmpeg/bin/ffmpeg'

# Remind console user of the prefix
print(f'Attempting to launch Bot using {prefix} as the command prefix.')

# Song List
print('Initializing Song Library')
songs = []
for r, d, f in os.walk('music'):
    for file in f:
        if ".mp3" in file or ".wma" in file:
            songs.append(os.path.join(r, file))
print('Song Library Initialized')

#voiceClient Dictionary
voiceClientDictionary = {}

#initialize discord client
bot = discord.Client()

#set command prefix
bot = commands.Bot(command_prefix=prefix)

# use this function for creating an audioSource from an mp3 file
# from https://github.com/elibroftw/discord-bot/blob/master/bot.py
def create_audio_source(music_filepath,start_at=0.0):
    audio_source = FFmpegPCMAudio(music_filepath, executable=ffmpeg_path, options='-vn -b:a 128k')
    audio_source = PCMVolumeTransformer(audio_source)
    #audio_source.volume = guild_data['volume']
    return audio_source

# choose a song at random
def random_song():
    return choice(songs)

# if the bot is ready print that out.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

# ping command for testing purposes
@bot.command(name = 'ping')
async def ping(ctx):
    await ctx.send('Pong!')

# join command to summon the bot to the voicechannel the user is in
@bot.command(name = 'join')
async def join(ctx):
    # set vc to the voiceclient out of the dictionary, if there isn't one this will be 'none'
    vc = voiceClientDictionary.get(ctx.guild.id)
    # set channel to the author's voice channel, also possibly 'none'
    channel = ctx.author.voice.channel
    # if the author is not in a VC
    if not channel:
        # send an error and return
        await ctx.send('You\'re not in a voice channel.')
        return None
    # if there isn't a client in the dictionary
    if not vc:
        #connect to the users channel and store that value in the dict.
        vc = await channel.connect()
        voiceClientDictionary[ctx.guild.id] = vc
        # this is here to force an await after altering the dict.
        await ctx.send('Ready.')
    # if the user isn't in the channel that the bot is, move the bot.
    elif vc.channel != channel:
        await vc.move_to(channel)
    return vc


# disconnect command
@bot.command(name = 'leave', aliases = ['disconnect','go','goaway'])
async def leave(ctx):
    # set vc to the voiceclient out of the dictionary, if there isn't one this will be 'none'
    vc = voiceClientDictionary.get(ctx.guild.id)
    # if there is a VC for the guild disconnect it, otherwise send an error
    if vc:
        await vc.disconnect()
        voiceClientDictionary.pop(ctx.guild.id, None)
        await ctx.send('Disconnected.')
    else:
        await ctx.send('I am not connected to a voice channel in this server.')

# play an audioSource
@bot.command(name = 'play')
async def play(ctx):
    # set vc to the voiceclient out of the dictionary, if there isn't one this will be 'none'
    vc = voiceClientDictionary.get(ctx.guild.id)
    # get the voice channel the author is in, this can be 'none'
    channel = ctx.author.voice.channel
    # if the author isn't in a channel, error out and return
    if not channel:
        await ctx.send('You\'re not in a voice channel.')
        return
    # if there isn't a vc, make one and add it to the dict.
    if not vc:
        vc = await channel.connect()
        voiceClientDictionary[ctx.guild.id] = vc
        await ctx.send('Ready')
    # if the user isn't in the channel with the bot, move the bot.
    if vc.channel != channel:
        await vc.move_to(channel)
    # if there's already audio playing stop it
    if vc.is_playing():
        vc.stop()
    # pick a random song and play it.
    song = random_song()    
    source = create_audio_source(song)
    vc.play(source)
    await ctx.send(f'Now Playing: {song}')

bot.run(token)