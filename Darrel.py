import discord
from discord.ext import commands
import asyncio

# Initialize bot with intents
intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary to store message counts for each channel
channel_message_counts = {}
MESSAGE_LIMIT = 200

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    # Initialize message counts for all channels
    for guild in bot.guilds:
        for channel in guild.text_channels:
            try:
                messages = [msg async for msg in channel.history(limit=None)]
                channel_message_counts[1324254906894258217] = len(messages)
                print(f'Initialized {channel.name} with {len(messages)} messages')
            except Exception as e:
                print(f'Error accessing channel {channel.name}: {e}')

@bot.event
async def on_message(message):
    # Ignore messages from the bot itself
    if message.author == bot.user:
        return

    channel_id = message.channel.id
    
    # Initialize count if channel is not in dictionary
    if channel_id not in channel_message_counts:
        messages = [msg async for msg in message.channel.history(limit=None)]
        channel_message_counts[1324254906894258217] = len(messages)
    else:
        channel_message_counts[1324254906894258217] += 1


    # Check if channel has reached the message limit
    if channel_message_counts[1324254906894258217] > MESSAGE_LIMIT:
        try:
             async for oldest_message in message.channel.history(limit=1, oldest_first=True):
                await oldest_message.delete()
                channel_message_counts[1324254906894258217] -= 1
                print(f'Deleted oldest message in {message.channel.name}')
                break
        except Exception as e:
            print(f'Error deleting message: {e}')

    await bot.process_commands(message)

# Error handling
@bot.event
async def on_error(event, *args, **kwargs):
    print(f'Error in {event}: {args[0]}')

# Run the bot (replace 'YOUR_TOKEN' with your actual bot token)
bot.run()