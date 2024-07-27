import discord
from discord.ext import commands
import asyncio
import youtube_dl
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pydub
from pydub import AudioSegment
from utils.music_player import MusicPlayer
from utils.helpers import create_embed
from config import secrets

# Suppress noisy yt-dlp logging
youtube_dl.utils.bug_reports_message = lambda: ''

class MusicCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_players = {}  # Store music players per guild

        # Spotify API client
        self.spotify_client_credentials_manager = SpotifyClientCredentials(
            client_id=secrets.SPOTIFY_CLIENT_ID,
            client_secret=secrets.SPOTIFY_CLIENT_SECRET
        )
        self.spotify = spotipy.Spotify(client_credentials_manager=self.spotify_client_credentials_manager)

    @commands.command(name="play", help="Plays a song from YouTube or Spotify.")
    async def play(self, ctx, *, query):
        """Plays a song from YouTube or Spotify."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id not in self.music_players:
                self.music_players[ctx.guild.id] = MusicPlayer(voice_channel)
            music_player = self.music_players[ctx.guild.id]

            if "youtube.com" in query or "youtu.be" in query:
                # Play from YouTube
                try:
                    info = youtube_dl.YoutubeDL({}).extract_info(query, download=False)
                    url = info['formats'][0]['url']
                    song_title = info['title']

                    await music_player.add_song(url, song_title)
                    await ctx.send(embed=create_embed(title="Added to Queue", description=f"{song_title} added to the queue."))

                except Exception as e:
                    print(f"Error playing YouTube song: {e}")
                    await ctx.send(embed=create_embed(title="Error", description="Failed to play the YouTube song. Please check the URL."))

            elif "spotify.com" in query:
                # Play from Spotify
                try:
                    # Get the Spotify track ID from the URL
                    track_id = query.split("/")[-1]
                    track_info = self.spotify.track(track_id)
                    song_title = track_info['name']

                    # Get the track's audio preview URL
                    audio_preview_url = track_info['preview_url']
                    if audio_preview_url is None:
                        await ctx.send(embed=create_embed(title="Error", description="This Spotify track doesn't have an audio preview."))
                        return
                    
                    # Add the preview URL to the queue
                    await music_player.add_song(audio_preview_url, song_title)
                    await ctx.send(embed=create_embed(title="Added to Queue", description=f"{song_title} added to the queue."))

                except Exception as e:
                    print(f"Error playing Spotify song: {e}")
                    await ctx.send(embed=create_embed(title="Error", description="Failed to play the Spotify song. Please check the URL."))

            else:
                await ctx.send(embed=create_embed(title="Error", description="Invalid URL. Please provide a valid YouTube or Spotify link."))

            if not music_player.is_playing:
                await music_player.play_next()

        except Exception as e:
            print(f"Error in play command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while playing the song."))

    @commands.command(name="pause", help="Pauses the currently playing song.")
    async def pause(self, ctx):
        """Pauses the currently playing song."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id in self.music_players:
                music_player = self.music_players[ctx.guild.id]
                if music_player.is_playing:
                    await music_player.pause()
                    await ctx.send(embed=create_embed(title="Paused", description="Music paused."))
                else:
                    await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))
            else:
                await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))

        except Exception as e:
            print(f"Error in pause command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while pausing the music."))

    @commands.command(name="resume", help="Resumes playback of the paused song.")
    async def resume(self, ctx):
        """Resumes playback of the paused song."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id in self.music_players:
                music_player = self.music_players[ctx.guild.id]
                if music_player.is_paused:
                    await music_player.resume()
                    await ctx.send(embed=create_embed(title="Resumed", description="Music resumed."))
                else:
                    await ctx.send(embed=create_embed(title="Error", description="No music is currently paused."))
            else:
                await ctx.send(embed=create_embed(title="Error", description="No music is currently paused."))

        except Exception as e:
            print(f"Error in resume command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while resuming the music."))

    @commands.command(name="skip", help="Skips to the next song in the queue.")
    async def skip(self, ctx):
        """Skips to the next song in the queue."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id in self.music_players:
                music_player = self.music_players[ctx.guild.id]
                if music_player.is_playing:
                    await music_player.skip()
                    await ctx.send(embed=create_embed(title="Skipped", description="Skipped to the next song."))
                else:
                    await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))
            else:
                await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))

        except Exception as e:
            print(f"Error in skip command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while skipping the song."))

    @commands.command(name="stop", help="Stops playback and clears the queue.")
    async def stop(self, ctx):
        """Stops playback and clears the queue."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id in self.music_players:
                music_player = self.music_players[ctx.guild.id]
                await music_player.stop()
                await ctx.send(embed=create_embed(title="Stopped", description="Music stopped and queue cleared."))
            else:
                await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))

        except Exception as e:
            print(f"Error in stop command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while stopping the music."))

    @commands.command(name="queue", help="Displays the current queue of songs.")
    async def queue(self, ctx):
        """Displays the current queue of songs."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id in self.music_players:
                music_player = self.music_players[ctx.guild.id]
                queue = music_player.queue

                if len(queue) == 0:
                    await ctx.send(embed=create_embed(title="Queue", description="The queue is empty."))
                    return

                embed = create_embed(title="Queue", description=f"**Now Playing:** {music_player.current_song}\n\n**Up Next:**\n{'\n'.join(f'{i+1}. {song}' for i, song in enumerate(queue))}")
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))

        except Exception as e:
            print(f"Error in queue command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while displaying the queue."))

    @commands.command(name="volume", help="Sets the volume of the music player. (0-100)")
    async def volume(self, ctx, volume: int):
        """Sets the volume of the music player. (0-100)"""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if ctx.guild.id in self.music_players:
                music_player = self.music_players[ctx.guild.id]
                if 0 <= volume <= 100:
                    await music_player.set_volume(volume / 100)
                    await ctx.send(embed=create_embed(title="Volume Set", description=f"Volume set to {volume}%."))
                else:
                    await ctx.send(embed=create_embed(title="Error", description="Volume must be between 0 and 100."))
            else:
                await ctx.send(embed=create_embed(title="Error", description="No music is currently playing."))

        except Exception as e:
            print(f"Error in volume command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while setting the volume."))

    @commands.command(name="search", help="Searches for a song on YouTube or Spotify.")
    async def search(self, ctx, *, query):
        """Searches for a song on YouTube or Spotify."""

        try:
            voice_channel = ctx.author.voice.channel
            if voice_channel is None:
                await ctx.send(embed=create_embed(title="Error", description="You must be in a voice channel to use this command."))
                return

            if "youtube.com" in query or "youtu.be" in query:
                # Search on YouTube
                try:
                    info = youtube_dl.YoutubeDL({}).extract_info(query, download=False)
                    results = info['entries']
                    if results is None:
                        await ctx.send(embed=create_embed(title="Error", description="No results found for this YouTube query."))
                        return

                    embed = create_embed(title="YouTube Search Results", description="\n".join(f"{i+1}. {result['title']}" for i, result in enumerate(results)))
                    await ctx.send(embed=embed)

                except Exception as e:
                    print(f"Error searching YouTube: {e}")
                    await ctx.send(embed=create_embed(title="Error", description="Failed to search YouTube. Please check your query."))

            elif "spotify.com" in query:
                # Search on Spotify
                try:
                    results = self.spotify.search(q=query, type="track", limit=5)
                    tracks = results['tracks']['items']
                    if len(tracks) == 0:
                        await ctx.send(embed=create_embed(title="Error", description="No results found for this Spotify query."))
                        return

                    embed = create_embed(title="Spotify Search Results", description="\n".join(f"{i+1}. {track['name']} - {track['artists'][0]['name']}" for i, track in enumerate(tracks)))
                    await ctx.send(embed=embed)

                except Exception as e:
                    print(f"Error searching Spotify: {e}")
                    await ctx.send(embed=create_embed(title="Error", description="Failed to search Spotify. Please check your query."))

            else:
                await ctx.send(embed=create_embed(title="Error", description="Invalid URL. Please provide a valid YouTube or Spotify link."))

        except Exception as e:
            print(f"Error in search command: {e}")
            await ctx.send(embed=create_embed(title="Error", description="An error occurred while searching for the song."))

# Add the music cog to the bot
def setup(bot):
    bot.add_cog(MusicCog(bot))