import discord
from discord.ext import commands

bot = discord.Bot(intents=discord.Intents.all())

class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot.command(description="幫助訊息")
    async def help(self, ctx):
        embed = discord.Embed(
            title="幫助訊息",
            description=(
                f"你好{ctx.author.mention}😀，\n"
                f"我是一臺由古叡宸製作的AI機器人🤖，\n"
                f"當你看到我在線上時，\n"
                f"，歡迎直接在私人頻道和我一起聊天💬\n"
                f"你可以使用！加上內容與AI對話📢，"
                f"也可以附上圖片讓我判斷🏞️，\n"
                f"每天第一次和我對話時我的回話速度比較慢，很抱歉😓\n"
                f"還有 /weather、/earthquake 指令獲得天氣或地震資訊🌥️。\n"
                f"或是使用 /generate_qrcode 建立自己QR code。"
            ),
            color=discord.Color.blue()
        )
        await ctx.respond(embed=embed, ephemeral=True)

def setup(bot):
    bot.add_cog(help(bot))