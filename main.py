import os
import toml
from mcstatus import MinecraftServer
import discord
from discord.ext import commands
import platform
import subprocess
import time


test_all = ["SERVER_TOKEN", "SERVER_IP", "SERVER_PORT", "SERVER_PREFIX"]

for string in test_all:
    try:
        if os.environ[string] != "":
            print("{} not supplied using docker environment variables, use this as ref https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file".format(string))
            quit()
    except:
        config = toml.load("config.toml")
        if (config[string] == None):
            print("{} not supplied in config.toml".format(string))
            quit()

ref_time = time.localtime()


TOKEN = config["token"]
host = config["ip"] + ":" + config["port"]
server = MinecraftServer.lookup(host)
prefix = config["prefix"]

bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
print("Triton started")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('!status'):
        cur_time = time.strftime("%H:%M:%S", ref_time)
        if (ping(config["ip"])):
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

    if message.content.startswith('!query'):
        cur_time = time.strftime("%H:%M:%S", ref_time)
        if (ping(config["ip"])):
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

def ping(host):
    param = '-n' if platform.system().lower()=='windows' else '-c'

    command = ['ping', param, '1', host]

    return subprocess.call(command) == 0


bot.run(TOKEN)