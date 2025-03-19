import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv

load_dotenv('/home/grundy/PycharmProjects/diplo/.env')
discord_bot_token = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True  # Enable the intent to read message content

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def test(ctx, *, text: str):
    response = requests.post(
        'http://127.0.0.1:8889/process_query',
        json={'text': text}
    )
    result = response.json()
    await ctx.send(result)

bot.run(discord_bot_token)