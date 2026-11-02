import os
import discord
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"「{bot.user}」已成功在雲端登入！")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    if message.content == "hi":
        await message.channel.send("Hello!")

@bot.command(description="回復world")
async def hello(ctx):
    await ctx.respond("world")

# 啟動防休眠伺服器
keep_alive()

# 從 Render 環境變數讀取 Token
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
