# settings should have prefix and token variables
from settings import *
# get audio utilities specifically
from discord import FFmpegPCMAudio, PCMVolumeTransformer

# import discord python library
import discord
# import the command module
from discord.ext import commands

# set the filepath for the audio decoder
ffmpeg_path = ffmpeg_path = 'ffmpeg/bin/ffmpeg'

# Remind console user of the prefix
print(f'Attempting to launch Bot using {prefix} as the command prefix.')

#initialize discord client
bot = discord.Client()

#set command prefix
bot = commands.Bot(command_prefix=prefix)

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
    channel = ctx.author.voice.channel
    await channel.connect()

# use this function for creating an audioSource from an mp3 file
# from https://github.com/elibroftw/discord-bot/blob/master/bot.py
def create_audio_source(start_at=0.0):
    # music_filepath = 'f'Music/{song.get_video_id()}'.mp3'
    music_filepath = 'music/trog.mp3'
    audio_source = FFmpegPCMAudio(music_filepath, executable=ffmpeg_path,
                                  options='-vn -b:a 128k')
    audio_source = PCMVolumeTransformer(audio_source)
    #audio_source.volume = guild_data['volume']
    return audio_source

# play an audioSource
@bot.command(name = 'play')
async def play(ctx):
    channel = ctx.author.voice.channel
    vc = await channel.connect()

    source = create_audio_source()
    vc.play(source)

bot.run(token)