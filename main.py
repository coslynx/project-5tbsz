import discord
from discord.ext import commands
import os
import asyncio

from config import secrets, database

# Load environment variables from .env file
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()

# Define bot prefix
bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# Load cogs
async def load_cogs():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")

# Set up database connection
async def setup_database():
    if database.DATABASE_TYPE == "postgres":
        from database.models import db
        db.init_app(bot)
    elif database.DATABASE_TYPE == "mongodb":
        from database.models import db
        db.init_app(bot)
    else:
        print("Invalid database type. Please specify 'postgres' or 'mongodb' in .env.")
        await bot.close()
        return

# Event handler for bot ready event
@bot.event
async def on_ready():
    await load_cogs()
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    print("------------------------------------")

# Run the bot
async def main():
    await setup_database()
    await bot.start(secrets.DISCORD_BOT_TOKEN)

if __name__ == '__main__':
    asyncio.run(main())