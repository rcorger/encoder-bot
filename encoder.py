import discord
from discord.ext import commands
from discord.ext.commands.context import Context
import json
import os
from stegano import lsb
import requests

intents = discord.Intents.all()

with open("./config.json") as f:
    conf = json.loads(f.read())

prefix = conf["PREFIX"]
client = commands.Bot(command_prefix=prefix, intents=intents)

@client.event
async def on_ready():
    print(f"noob {client.user.name} is running with pid of", os.getpid())

@client.command()
async def encode(ctx: Context):
    if ctx.guild is not None:
        return await ctx.reply("I only work in dms ;)")

    encoding_msg = ' '.join(ctx.message.content.split(' ')[1::]).strip()
    if encoding_msg == "":
        return await ctx.reply("You must provide a message to encode into the image!")
    
    try:
        attachment_url = ctx.message.attachments[0].url
    except:
        await ctx.reply("No image was supplied!")
    file_request = requests.get(attachment_url)

    with open("uploadedfile.png", "wb+") as f:
        f.write(file_request.content)
    
    secret = lsb.hide('./uploadedfile.png', encoding_msg)
    secret.save('./uploadedfile.png')

    with open('./uploadedfile.png', 'rb') as f:
        picture = discord.File(f)
        await ctx.reply("Here is your encoded picture(message)", file=picture)
        
    os.remove("./uploadedfile.png")

@client.command()
async def decode(ctx: Context):
    if ctx.guild is not None:
        return await ctx.reply("I only work in dms ;)")
    
    try:
        attachment_url = ctx.message.attachments[0].url
    except:
        await ctx.reply("No image was supplied!")
    file_request = requests.get(attachment_url)

    with open("uploadedfile.png", "wb+") as f:
        f.write(file_request.content)
    
    secret = lsb.reveal('./uploadedfile.png')

    await ctx.reply(f"The encoded message within that image was:```{secret}```")
        
    os.remove("./uploadedfile.png")

client.run(conf["TOKEN"], log_handler=None) # no handler cause it looks shitty.
