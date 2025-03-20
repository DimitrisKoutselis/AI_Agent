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
    content = result

    print(f"\n\n\n\n\n\n\n{result}\n\n\n\n\n\n\n")
    parts = content.split('\n-------------------------\n')
    current_part = ""

    if (not "Condition" in content) and (not "Low" in content) and (not "High" in content) and "\n-------------------------\n" in content:
        for part in parts[:5]:
            if len(current_part) + len(part) + len('\n-------------------------\n') > 2000:
                await ctx.send(current_part.strip())
                current_part = part + '\n-------------------------\n'
            else:
                current_part += part + '\n-------------------------\n'

        if current_part.strip():
            await ctx.send(current_part.strip())

    else:
        await ctx.send(result)


@bot.command()
async def table(ctx):
    embed = discord.Embed(title="User Info", color=discord.Color.blue())
    embed.add_field(name="Name", value="John\nAlice\nBob", inline=True)
    embed.add_field(name="Age", value="22\n19\n25", inline=True)
    embed.add_field(name="Role", value="Moderator\nMember\nAdmin", inline=True)

    await ctx.send(embed=embed)

bot.run(discord_bot_token)
