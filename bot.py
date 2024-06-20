import discord
import asyncio
import os
from dotenv import load_dotenv

from figgs.figgs import figgs
from discord.ext import commands

load_dotenv()

Client = commands.Bot(command_prefix="!", intents=discord.Intents.all())

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
            s = figgs(auth=os.getenv("FIGGS_AUTH_KEY"))
            s.change_user_name(author.name)
            
            room_id = os.getenv("ROOM_ID")
            bot_id = os.getenv("BOT_ID")
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
Client.run(os.getenv("BOT_TOKEN"))
