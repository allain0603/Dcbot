import os
import discord
import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands
from discord.ui import Select, View
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

# 高醫大 7 大學院與教務總覽資料庫
KMU_COLLEGES = {
    "med": {
        "name": "醫學院",
        "url": "https://cmed.kmu.edu.tw/",
        "depts": ["醫學系", "學士後醫學系", "生物學系", "生物醫學檢驗學系", "醫學影像暨放射科學系"]
    },
    "dent": {
        "name": "牙醫學院",
        "url": "https://dent.kmu.edu.tw/",
        "depts": ["牙醫學系", "口腔衛生學系"]
    },
    "pharm": {
        "name": "藥學院",
        "url": "https://cpharm.kmu.edu.tw/",
        "depts": ["藥學系", "香妝品學系"]
    },
    "nursing": {
        "name": "護理學院",
        "url": "https://con.kmu.edu.tw/",
        "depts": ["護理學系", "高齡長期照護碩士學位學程"]
    },
    "health": {
        "name": "健康科學院",
        "url": "https://chs.kmu.edu.tw/",
        "depts": ["公共衛生學系", "物理治療學系", "職能治療學系", "醫務管理暨醫療資訊學系", "醫用應用化學系"]
    },
    "life": {
        "name": "生命科學院",
        "url": "https://clss.kmu.edu.tw/",
        "depts": ["生物科技學系", "醫學社會學與社會工作學系"]
    },
    "human": {
        "name": "人文社會科學院",
        "url": "https://chss.kmu.edu.tw/",
        "depts": ["心理學系", "正向心理學碩士班"]
    },
    "academic": {
        "name": "教務處（轉系/雙主修/輔系專區）",
        "url": "https://academic.kmu.edu.tw/",
        "depts": ["轉系申請規定", "雙主修/輔系法規", "跨領域學分學程"]
    }
}

class KMUCollegeSelect(Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="轉系/雙主修/輔系資訊", value="academic", description="教務處轉系、雙主修與輔系規定", emoji="📜"),
            discord.SelectOption(label="1. 醫學院", value="med", description="醫學系、後醫系、生檢系、放視系等", emoji="🩺"),
            discord.SelectOption(label="2. 牙醫學院", value="dent", description="牙醫學系、口腔衛生學系", emoji="🦷"),
            discord.SelectOption(label="3. 藥學院", value="pharm", description="藥學系、香妝品學系", emoji="💊"),
            discord.SelectOption(label="4. 護理學院", value="nursing", description="護理學系、長照學程", emoji="🏥"),
            discord.SelectOption(label="5. 健康科學院", value="health", description="公衛系、物治系、職治系、醫管資系、應化系", emoji="🔬"),
            discord.SelectOption(label="6. 生命科學院", value="life", description="生技系、醫社系", emoji="🧬"),
            discord.SelectOption(label="7. 人文社會科學院", value="human", description="心理學系等", emoji="🧠")
        ]
        super().__init__(placeholder="請選擇高醫大的學院或教務項目...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        target = KMU_COLLEGES.get(self.values[0])
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
        
        dept_str = "\n".join([f"• {dept}" for dept in target["depts"]])
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(target["url"], headers=headers, timeout=10) as response:
                    if response.status == 200:
                        html = await response.text()
                        soup = BeautifulSoup(html, "html.parser")
                        
                        # 自動擷取該學院網站上的公告標題
                        announcements = []
                        for a in soup.find_all("a"):
                            text = a.text.strip()
                            if len(text) > 8 and ("公告" in text or "簡章" in text or "學年度" in text or "招生" in text):
                                if text not in announcements:
                                    announcements.append(text)
                            if len(announcements) >= 3:
                                break
                        
                        reply = f"🏫 **高雄醫學大學 - {target['name']}**\n"
                        reply += f"🔗 官網網址：{target['url']}\n\n"
                        reply += f"📋 **包含科系/單位**：\n{dept_str}\n\n"
                        
                        if announcements:
                            reply += "📰 **院所最新重要公告**：\n"
                            for idx, ann in enumerate(announcements, 1):
                                reply += f"{idx}. {ann}\n"
                        
                        await interaction.followup.send(reply)
                    else:
                        await interaction.followup.send(f"🏫 **{target['name']}**\n🔗 網址：{target['url']}\n\n📋 **包含科系/單位**：\n{dept_str}")
        except Exception as e:
            await interaction.followup.send(f"🏫 **{target['name']}**\n🔗 網址：{target['url']}\n\n📋 **包含科系/單位**：\n{dept_str}\n\n*(自動連線擷取即時新聞時超時，但科系名單如上)*")

class KMUView(View):
    def __init__(self):
        super().__init__()
        self.add_item(KMUCollegeSelect())

@bot.event
async def on_ready():
    print(f"「{bot.user}」已成功在雲端登入！")

@bot.command(description="高醫大全校學院與科系查詢導覽")
async def kmu(ctx):
    await ctx.respond("🎓 **高雄醫學大學全校科系導覽系統**\n請點擊下方選單選擇你想查詢的學院：", view=KMUView())

keep_alive()
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
