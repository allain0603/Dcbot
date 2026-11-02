import os
import discord
import aiohttp
from bs4 import BeautifulSoup
from discord.ext import commands
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print(f"「{bot.user}」已成功在雲端登入！")

@bot.command(description="讀取並解析高醫大最新公告頁面 HTML")
async def fetch_kmu_news(ctx):
    # 延遲回應，避免網路請求耗時導致 Discord 指令逾時
    await ctx.defer()
    
    # 目標 HTML 網址：高醫大最新公告頁面
    url = "https://www.kmu.edu.tw/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        # 1. 透過 aiohttp 抓取原始 HTML
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, timeout=10) as response:
                if response.status == 200:
                    html_text = await response.text()
                    
                    # 2. 透過 BeautifulSoup 解析 HTML 結構
                    soup = BeautifulSoup(html_text, "html.parser")
                    
                    # 抓取 <title> 標籤
                    page_title = soup.title.string.strip() if soup.title else "無標題"
                    
                    # 抓取頁面中所有包含超連結 <a> 的標籤並解析文字與 href 屬性
                    news_items = []
                    for a_tag in soup.find_all("a", href=True):
                        text = a_tag.text.strip()
                        href = a_tag["href"]
                        
                        # 補全相對路徑 (Relative URL)
                        if href.startswith("/"):
                            href = "https://www.kmu.edu.tw" + href
                        elif not href.startswith("http"):
                            continue

                        # 篩選長度大於 6 個字且包含公告/關鍵字之標題
                        if len(text) >= 6 and text not in [n['title'] for n in news_items]:
                            news_items.append({"title": text, "link": href})
                            
                        if len(news_items) >= 5: # 先印出前 5 筆進行 HTML 測試
                            break

                    # 3. 組合解析結果
                    if news_items:
                        result_msg = f"📄 **HTML 讀取成功！**\n📌 **網頁標題**：`{page_title}`\n\n🔍 **解析出的最新公告標題與 HTML 超連結**：\n"
                        for idx, item in enumerate(news_items, 1):
                            result_msg += f"{idx}. [{item['title']}]({item['link']})\n"
                        await ctx.followup.send(result_msg)
                    else:
                        await ctx.followup.send(f"📄 HTML 讀取成功（標題：`{page_title}`），但未解析出符合條件的公告連結。")
                else:
                    await ctx.followup.send(f"❌ HTML 讀取失敗，伺服器狀態碼：{response.status}")
    except Exception as e:
        await ctx.followup.send(f"⚠️ 解析 HTML 時發生錯誤：{e}")

# 啟動防休眠 Web 伺服器
keep_alive()

# 讀取 Token 並啟動 Bot
TOKEN = os.getenv("DISCORD_TOKEN")
bot.run(TOKEN)
