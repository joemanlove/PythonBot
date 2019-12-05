# settings should have prefix and token variables
from settings import *
# get audio utilities specifically
from discord import FFmpegPCMAudio, PCMVolumeTransformer
# get os for filesystem navigation
import os
# get the random.choice function
from random import choice
# import the math library
import math
# import discord python library
import discord
# import the command module
from discord.ext import commands

import asyncio

# set the filepath for the audio decoder
ffmpeg_path = 'ffmpeg/bin/ffmpeg'

# Remind console user of the prefix
print(f'Attempting to launch Bot using {prefix} as the command prefix.')

# voiceClient Dictionary
voiceClientDictionary = {}

# play on loop Dictionary
autoPlayDictionary = {}

# initialize discord client
bot = discord.Client()

# set command prefix
bot = commands.Bot(command_prefix=prefix)

# class for songs
class Song:
    # constructor, also sets path
    def __init__(self,_artist,_album,_title):
        self.artist = _artist
        self.album = _album
        self.title = _title
        self.path = f'music/{self.artist}/{self.album}/{self.title}'
    
    # display method, returns string
    def displayTitle(self):
       return f'Now playing:\n{self.title}\nby -> {self.artist}\non the album -> {self.album}'

# loop through the directory stuctures and make songs.
def populateSongList():
    songList = []
    for artist in os.listdir('music'):
        if os.path.isdir(f'music/{artist}'):
            for album in os.listdir(f'music/{artist}'):
                if os.path.isdir(f'music/{artist}/{album}'):
                    for f in os.listdir(f'music/{artist}/{album}'):
                        if ".mp3" in f or ".wma" in f:
                            songList.append(Song(artist, album, f))
    if songList == []:
        print('Warning empty Song Library.\n Check your file structure and terminal directory.')
    return songList

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

# Song List
print('Initializing Song Library')
songs = populateSongList()
print(f'Song Library Initialized with {len(songs)} items.')

# if the bot is ready print that out.
@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    bot.loop.create_task(status_task())




# ping command for testing purposes
@bot.command(name = 'ping')
async def ping(ctx):
    await ctx.send('Pong!')

async def setUpVoiceClient(ctx):
    # set vc to the voiceclient out of the dictionary, if there isn't one this will be 'none'
    vc = voiceClientDictionary.get(ctx.guild.id)
    # set channel to the author's voice channel, also possibly 'none'
    if ctx.author.voice:
        channel = ctx.author.voice.channel
    else:
        channel = False
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


# join command to summon the bot to the voicechannel the user is in
@bot.command(name = 'join')
async def join(ctx):
    await setUpVoiceClient(ctx)


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
    # get a voiceClient up and running or fetch the existing one
    vc = await setUpVoiceClient(ctx)
    
    if vc.is_playing():
        vc.stop()
    # pick a random song and play it.
    song = random_song()    
    source = create_audio_source(song.path)
    vc.play(source)
    # await ctx.send(f'Now Playing: {song.title}')
    await ctx.send(song.displayTitle())

def playRandomSong(vc):
    song = random_song()    
    source = create_audio_source(song.path)
    vc.play(source)
    return song.displayTitle()

@bot.command(name = 'autoplay')
async def autoplay(ctx):
    # get a voiceClient up and running or fetch the existing one
    vc = await setUpVoiceClient(ctx)
    autoPlayDictionary[ctx.guild.id] = True
    

@bot.command(name = 'source')
async def source(ctx):
    # read in the source file
    f = open('main.py','r')
    contents = f.read()
    f.close()

    # initialize a list of content to send
    contentList = []

    # cut the sourcecode into manageable sized chunks
    for i in range(math.ceil(len(contents)/1900)):
        contentList.append(contents[:1900])
        contents = contents[1900:]

    # send each chunk in it's own message
    for chunk in contentList:
        # these kimda jackup the formatting, which is a little funny.
        await ctx.send('```' + chunk + '```')

async def status_task():
    while True:
        for guildId in voiceClientDictionary.keys():
            # print(guildId)
            # extend the voiceClient instead, this is silly.
            vc = voiceClientDictionary.get(guildId)
            if autoPlayDictionary.get(guildId) and vc:
                if not vc.is_playing():
                    st = playRandomSong(vc)
                    print(st)
                
        await asyncio.sleep(10)
        # print('1')
        # await asyncio.sleep(10)
        # print('2')
        # await asyncio.sleep(10)


bot.run(token)