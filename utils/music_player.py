import discord
import asyncio
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from pydub import AudioSegment
from pydub.playback import play

class MusicPlayer:
    def __init__(self, voice_channel):
        self.voice_channel = voice_channel
        self.vc = None
        self.queue = []
        self.current_song = None
        self.is_playing = False
        self.is_paused = False
        self.volume = 0.5

    async def connect(self):
        """Connects the bot to the voice channel."""
        self.vc = await self.voice_channel.connect()

    async def disconnect(self):
        """Disconnects the bot from the voice channel."""
        if self.vc:
            await self.vc.disconnect()

    async def add_song(self, url, song_title):
        """Adds a song to the queue."""
        self.queue.append((url, song_title))

    async def play_next(self):
        """Plays the next song in the queue."""
        if len(self.queue) > 0:
            self.current_song = self.queue.pop(0)
            url, song_title = self.current_song
            
            try:
                # Check if the song is a Spotify URL 
                if "spotify.com" in url:
                    # Get the track's audio preview URL using spotipy
                    track_id = url.split("/")[-1]
                    track_info = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials()).track(track_id)
                    audio_preview_url = track_info['preview_url']

                    # Download and play the audio preview 
                    if audio_preview_url is not None:
                        ydl_opts = {'format': 'bestaudio'}
                        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                            info = ydl.extract_info(audio_preview_url, download=False)
                            url = info['formats'][0]['url']
                            audio = AudioSegment.from_file(url, format="mp3")
                            play(audio)
                            self.is_playing = True
                        await asyncio.sleep(audio.duration_seconds)
                        self.is_playing = False
                    else:
                        print("No audio preview available for this Spotify track.")
                        await self.play_next()  # Play the next song in the queue

                else:
                    # Play from YouTube
                    ydl_opts = {'format': 'bestaudio'}
                    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                        info = ydl.extract_info(url, download=False)
                        url = info['formats'][0]['url']
                        audio = AudioSegment.from_file(url, format="mp3")
                        play(audio)
                        self.is_playing = True
                    await asyncio.sleep(audio.duration_seconds)
                    self.is_playing = False

                await self.play_next()  # Play the next song in the queue

            except Exception as e:
                print(f"Error playing song: {e}")

    async def pause(self):
        """Pauses the currently playing song."""
        if self.vc and self.vc.is_playing():
            self.vc.pause()
            self.is_playing = False
            self.is_paused = True

    async def resume(self):
        """Resumes playback of the paused song."""
        if self.vc and self.is_paused:
            self.vc.resume()
            self.is_playing = True
            self.is_paused = False

    async def skip(self):
        """Skips to the next song in the queue."""
        if self.vc:
            self.vc.stop()
            self.is_playing = False
            self.current_song = None
            await self.play_next()

    async def stop(self):
        """Stops playback and clears the queue."""
        if self.vc:
            self.vc.stop()
            self.is_playing = False
            self.is_paused = False
            self.current_song = None
            self.queue = []
            await self.disconnect()

    async def set_volume(self, volume):
        """Sets the volume of the music player."""
        if self.vc and 0 <= volume <= 1:
            self.volume = volume
            self.vc.source = discord.PCMVolumeTransformer(self.vc.source, volume=self.volume)