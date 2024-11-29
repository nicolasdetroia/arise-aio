import discord
from discord.ext import commands
import requests
import asyncio
import csv
import glob
from dhooks import Webhook, Embed
import config
import os

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Welcome Message with ASCII Art
@bot.event
async def on_ready():
    print("\u001b[36m░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░")
    print("\u001b[36m░░░██╗░░░█████╗░░█████╗░░██╗░░██╗░██████╗░░█████╗░███████╗░█████╗░███████╗░░░")
    print("\u001b[36m░░██║░░░██╔══██╗██╔══██╗██╔═══╝░██╔════╝░██╔══██╗╚════██║██╔══██╗██╔════╝░░░")
    print("\u001b[36m░██║░░░░███████║██║░░██║██║░░██╗██║░░██╗░██║░░██║░░███╔═╝██║░░██║███████╗░░░")
    print("\u001b[36m░██║░░░░██╔══██║██║░░██║██║░░██║██║░░╚██╗██║░░██║██╔══╝░░██║░░██║██╔══╝░░░░░")
    print("\u001b[36m░██║░░░░██║░░██║╚█████╔╝╚█████╔╝╚██████╔╝╚█████╔╝███████╗╚█████╔╝███████╗░░░")
    print("\u001b[36m░░╚═╝░░░╚═╝░░╚═╝░╚════╝░░╚════╝░░╚═════╝░░╚════╝░░╚══════╝░╚════╝░╚══════╝░░░")
    print("\u001b[0m")
    print(f'Bot is logged in as {bot.user}')


# License Validation
@bot.command()
async def validate(ctx):
    try:
        with open("scratch.txt", "r") as a_file:
            list_of_lines = a_file.readlines()
        license_key = list_of_lines[2].split(":")[1].strip().replace('"', '').replace(',', '')
        headers = {'Authorization': f'Bearer {license_key}'}
        response = requests.get(f'https://api.hyper.co/v4/licenses/{license_key}', headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            user = user_data['user']['username']
            config.user = user
            await ctx.send(f'Welcome {user}! Your key is valid.')
        else:
            await ctx.send("Your key is invalid. Please provide a new key using `!setkey`.")
    except Exception as e:
        await ctx.send(f"Error during validation: {str(e)}")

@bot.command()
async def setkey(ctx, key):
    try:
        with open("scratch.txt", "r") as a_file:
            list_of_lines = a_file.readlines()
        list_of_lines[2] = f'    "key": "{key}",\n'
        with open("scratch.txt", "w") as a_file:
            a_file.writelines(list_of_lines)
        await ctx.send("Key updated successfully. Please run `!validate` to check its validity.")
    except Exception as e:
        await ctx.send(f"Error updating the key: {str(e)}")

# Task Menu
@bot.command()
async def tasks(ctx):
    try:
        filelist = glob.glob("Task Groups/*.csv")
        if not filelist:
            await ctx.send("No task groups found.")
            return
        await ctx.send("The following Groups are available:")
        for idx, file in enumerate(filelist):
            await ctx.send(f"{idx + 1}: {file}")
        await ctx.send("Reply with the group number to start tasks.")
    except Exception as e:
        await ctx.send(f"Error listing tasks: {str(e)}")

# Task Runner
@bot.command()
async def starttasks(ctx, group_number: int):
    try:
        filelist = glob.glob("Task Groups/*.csv")
        if group_number < 1 or group_number > len(filelist):
            await ctx.send("Invalid group number.")
            return
        selected_file = filelist[group_number - 1]
        await ctx.send(f"You chose {selected_file}")
        task_list = []
        with open(selected_file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            next(csv_reader)  # Skip header
            for row in csv_reader:
                task_list.append(f'{row[1]}({row[0]},"{row[3]}","{row[2]}","{row[4]}","{row[5]}")')

        async def run_tasks():
            for task in task_list:
                # Replace eval with proper task execution logic
                await ctx.send(f"Executing task: {task}")

        await run_tasks()
    except Exception as e:
        await ctx.send(f"Error starting tasks: {str(e)}")

# Webhook Setup
@bot.command()
async def webhook(ctx, url):
    try:
        hook = Webhook(url)
        embed = Embed(
            description="Test Webhook",
            color=0xE74C3C,
            timestamp='now'
        )
        image1 = 'https://media.discordapp.net/attachments/782329553107288095/831936574341644298/AIO.png?width=567&height=567'
        embed.set_author(name='ARISE-AIO', icon_url=image1)
        embed.set_footer(text='Ready', icon_url=image1)
        embed.add_field(name="Webhook is ready and working!", value="Let's cook!")
        embed.set_thumbnail(image1)
        hook.send(embed=embed)
        await ctx.send("Webhook added and tested successfully.")
    except Exception as e:
        await ctx.send(f"Error adding webhook: {str(e)}")

# Exit Command
@bot.command()
async def exitbot(ctx):
    await ctx.send("Bot shutting down...")
    await bot.close()

# Run the bot
bot.run("YOUR_DISCORD_BOT_TOKEN")
