

class Song:
    def __init__(self,_artist,_album,_title):
        self.artist = _artist
        self.album = _album
        self.title = _title
    
    def displayTitle(self):
        print(f'Now playing:\n{self.title}\nby -> {self.artist}\non the album -> {self.album}')



def populateSongList():
    songList = []
    for artist in os.listdir('music'):
        if os.path.isdir(f'music/{artist}'):
            for album in os.listdir(f'music/{artist}'):
                if os.path.isdir(f'music/{artist}/{album}'):
                    for f in os.listdir(f'music/{artist}/{album}'):
                        if ".mp3" in f or ".wma" in f:
                            songList.append(Song(artist, album, f))
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