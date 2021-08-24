import os
import toml
from mcstatus import MinecraftServer
import discord
from discord.ext import commands
import platform
import subprocess
import time

config = toml.load("config.toml")

try:
    TOKEN = os.environ["SERVER_TOKEN"]
    host = os.environ["SERVER_IP"] + ":" + os.environ["SERVER_PORT"]
    prefix = os.environ["SERVER_PREFIX"]
except:
    try:
        TOKEN = config["SERVER_TOKEN"]
        host = config["SERVER_IP"] + ":" + config["SERVER_PORT"]
        prefix = config["SERVER_PREFIX"]
    except:
        print("No enviroments pass into either docker or config.toml")
        exit()

server = MinecraftServer.lookup(host)

bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
print("Triton started")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith("{}status".format(prefix)):
        ref_time = time.localtime()
        cur_time = time.strftime("%H:%M:%S", ref_time)
        if (ping()):
            try:
                msg = server.status()
            except:
                send_out = "since {}, Status : ❌ DOWN ❌".format(cur_time)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=send_out, status=discord.Status.idle))
                await message.channel.send("IP is working but minecraft server isnt running")
            else:
                await message.channel.send("The server has {0} players and replied in {1} ms".format(msg.players.online, msg.latency))
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=send_out, status=discord.Status.online))
                send_out = "since {0}, Status : ✔️ UP ✔️ , Players : {1}".format(cur_time, msg.players.online)

    if message.content.startswith("{}query".format(prefix)):
        ref_time = time.localtime()
        cur_time = time.strftime("%H:%M:%S", ref_time)
        if (ping()):
            try:
                msg = server.status()
            except:
                send_out = "since {}, Status : ❌ DOWN ❌".format(cur_time)
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=send_out, status=discord.Status.idle))
                await message.channel.send("IP is working but minecraft server isnt running")
            else:
                try:
                    msg = server.query()
                except:
                    send_out = "since {0}, Status : ✔️ UP ✔️ , Players : {1}".format(cur_time, msg.players.online)
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=send_out, status=discord.Status.online))
                    await message.channel.send("IP is working, server is running but Admin hasnt enabled RCON in .properties")

                else:
                    send_out = "since {0}, Status : ✔️ UP ✔️ , Players : {1}".format(msg.players.online)
                    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=send_out, status=discord.Status.online))
                    await message.channel.send("The server has the following players online: {0}".format(", ".join(query.players.names)))

    if message.content.startswith("{}help".format(prefix)):
        await message.channel.send("```Heres the available commands\n - status\n - query```")


def ping():
    ip = host.split(":")[0]
    print(ip)
    
    param = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', param, '1', ip]

    return subprocess.call(command) == 0

bot.run(TOKEN)