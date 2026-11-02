from pathlib import Path
import discord
import datetime
import time
from keep_alive import keep_alive
from discord.ext import commands


print(f"\n\n"
      f"....########.....######........########.....#######....########....\n"
      f"....##.....##...##....##.......##.....##...##.....##......##.......\n"
      f"....##.....##...##.............##.....##...##.....##......##.......\n"
      f"....##.....##...##.............########....##.....##......##.......\n"
      f"....##.....##...##.............##.....##...##.....##......##.......\n"
      f"....##.....##...##....##.......##.....##...##.....##......##.......\n"
      f"....########.....######........########.....#######.......##.......\n")

bot = discord.Bot(intents=discord.Intents.all())

for cog in [p.stem for p in Path("cog").glob("*.py")]:
    bot.load_extension(f'cog.{cog}')
    print(f'new_load {cog}.')
print('Done.')
print("\n-------------------------------------------------------------------\n")

@bot.event
async def on_ready():
    activity = discord.Activity(
                type=discord.ActivityType.playing,  
                name="🤖/help"  
    )
    await bot.change_presence(activity=activity)
    print(f"「{bot.user}」已登入\n")
    print("\n-------------------------------------------------------------------\n")
    for guild in bot.guilds:
        print(f"伺服器: {guild.name} ({guild.id})")
        for channel in guild.text_channels:
            print(f"    頻道: {channel.name} ({channel.id})")
        print("\n")
    print("\n-------------------------------------------------------------------\n")

keep_alive()

TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
