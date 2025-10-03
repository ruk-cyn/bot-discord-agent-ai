import os
import discord
from discord.ext import commands
import aiohttp

WEBHOOK_URL = 'https://n8n.cynlive.com/webhook/agent-ai/discord'
TOKEN = 'MTQxNTk0MzI5MzMyMTM1MTE5OA.GQpaVJ.Q5XzHOGDtMnLm4DKjOlAgm9cw9uJGTWqCqGuLk'

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    channel_name = message.channel.name
    category_name = message.channel.category.name if message.channel.category else None

    discord_data = {
        "channel_id": str(message.channel.id),
        "channel_name": channel_name,
        "category_name": category_name,
        "discord_id": str(message.author.id),
        "username": message.author.name,
        "content": message.content
    }

    # เพิ่มเช็ค username
    if message.author.name not in ["Agent Stock", "Yumi"]:
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(WEBHOOK_URL, json=discord_data) as resp:
                    if resp.status == 200:
                        print("✅ Data sent to n8n successfully")
                    else:
                        print(f"⚠️ Failed to send data, status code: {resp.status}")
        except Exception as e:
            print(f"❌ Error sending data: {e}")

    await bot.process_commands(message)


bot.run(TOKEN)
