import discord
from discord.ext import commands, tasks
import requests
import asyncio

TOKEN = 'YOUR_DISCORD_BOT_TOKEN'
YOUTUBE_API_KEY = 'YOUR_YOUTUBE_API_KEY'
CHANNEL_ID = 'YOUR_YOUTUBE_CHANNEL_ID'
LAST_VIDEO_ID_FILE = 'last_video_id.txt'

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

def get_last_video_id():
    try:
        with open(LAST_VIDEO_ID_FILE, 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def set_last_video_id(video_id):
    with open(LAST_VIDEO_ID_FILE, 'w') as file:
        file.write(video_id)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')
    check_youtube.start()

@tasks.loop(seconds=5)
async def check_youtube():
    url = f'https://www.googleapis.com/youtube/v3/search?key={YOUTUBE_API_KEY}&channelId={CHANNEL_ID}&part=snippet,id&order=date&maxResults=1'
    response = requests.get(url)
    data = response.json()
    latest_video = data['items'][0]

    video_id = latest_video['id']['videoId']
    video_title = latest_video['snippet']['title']
    video_url = f'https://www.youtube.com/watch?v={video_id}'

    last_video_id = get_last_video_id()
    if video_id != last_video_id:
        channel = bot.get_channel(1338925346770255935)
        message = await channel.send(f'โย่!!มีคลิปใหม่ {video_title}\n{video_url}')
        
        # Schedule the message to be deleted after 5 days (432000 seconds)
        await asyncio.sleep(120)
        await message.delete()

        set_last_video_id(video_id)

bot.run(TOKEN)
