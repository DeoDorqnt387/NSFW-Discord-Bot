import discord
import asyncio
import os
from dotenv import load_dotenv

from figgs.figgs import figgs
from discord.ext import commands

load_dotenv()

Client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

auth = "your-figgasi-auth-key" # This is your . auth
roomId= "your-figgsai-room-id" # This is your . room_id
botId= "your-figgsai-bot-id" # This is your . bot_id
token = "your-discord-bot-token" # This is your . token

@Client.event
async def on_ready():
    await Client.tree.sync()
    await Client.change_presence(activity=discord.activity.Game(name="Game"),  #
                                 status=discord.Status.do_not_disturb) #invisible, offline, online, idle
    print(f"{Client.user.name} Bot Ready to Use...")
    print("-------------------")


@Client.event
async def on_message(message):
    member = message.author

    if member == Client.user:
        return    
    
    ctx = await Client.get_context(message)
    if Client.user.mentioned_in(message):
        try:
            user_msg = message.content
            await ctx.typing()

            author = ctx.author
            s = figgs(auth=auth)
            s.change_user_name(author.name)
            
            room_id = roomId
            bot_id = botId
            response = s.send_message(user_msg, room_id, bot_id)
            print(response)
            del_msg = "<|eot_id|>"
            reply = response.replace(del_msg, "")

            await asyncio.sleep(1)
            await ctx.reply(reply)
            await Client.process_commands(message)
        except Exception as e:
            print("an error occured: ", e)
    else:
        return
Client.run(token)
