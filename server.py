import asyncio
import logging
import requests
import platform
from telethon.sync import TelegramClient, events
from telethon.tl.custom.button import Button
from datetime import datetime, timedelta
import psutil

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Read API_ID, API_HASH, and BOT_TOKEN from config.env
with open("config.env") as f:
    for line in f:
        if line.startswith("API_ID"):
            API_ID = line.strip().split("=")[1].strip().replace("'", "")
        elif line.startswith("API_HASH"):
            API_HASH = line.strip().split("=")[1].strip().replace("'", "")
        elif line.startswith("BOT_TOKEN"):
            BOT_TOKEN = line.strip().split("=")[1].strip().replace("'", "")

# Dictionary to store sent messages per chat
sent_messages = {}

# Initialize Telegram client
client = TelegramClient("my_session", API_ID, API_HASH)

# Start the client
if BOT_TOKEN:
    client.start(bot_token=BOT_TOKEN)
else:
    client.start()

logger.info("Bot started and running...")


def get_system_uptime():
    boot_time_timestamp = psutil.boot_time()
    current_time = datetime.now().timestamp()
    uptime_seconds = current_time - boot_time_timestamp
    uptime_str = str(timedelta(seconds=uptime_seconds))
    return uptime_str


# Get public IP
def get_public_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        ip_info = response.json()
        public_ip = ip_info["ip"]
        return public_ip
    else:
        return None


# Function to get server status information
def get_server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")
    network_info = psutil.net_io_counters()

    server_info = (
        f"IP Address: {public_ip}\n"
        f"CPU Usage: {cpu_usage:.2f}%\n"
        f"RAM Usage: {ram_info.used / (1024 ** 3):.2f} GB / {ram_info.total / (1024 ** 3):.2f} GB\n"
        f"Disk Usage: {disk_info.used / (1024 ** 3):.2f} GB / {disk_info.total / (1024 ** 3):.2f} GB\n"
        f"Upload: {network_info.bytes_sent / (1024 ** 3):.2f} GB\n"
        f"Download: {network_info.bytes_recv / (1024 ** 3):.2f} GB\n"
    )

    return server_info


def get_system_info():
    # CPU Count
    cpu_count_physical = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)
    cpu_count_str = (
        f"\nCPU Count: {cpu_count_physical} physical, {cpu_count_logical} logical"
    )

    # CPU Frequency
    cpu_frequency = psutil.cpu_freq()
    if cpu_frequency is not None:
        cpu_freq_str = f"CPU Frequency:\n    Current: {cpu_frequency.current:.2f} MHz\n    Minimum: {cpu_frequency.min:.2f} MHz\n    Maximum: {cpu_frequency.max:.2f} MHz\n"
    else:
        cpu_freq_str = "CPU Frequency: Information not available\n"

    # Network Information
    network_info = psutil.net_if_stats()
    network_info_str = "Network Info:\n"
    for interface, stats in network_info.items():
        network_info_str += f"    Interface: {interface}\n        Speed: {stats.speed / 10 ** 6:.2f} Mbps\n        Is Up: {stats.isup}\n"
    network_info_str += ""

    # Combine all the information
    system_info = f"{cpu_count_str}\n{cpu_freq_str}{network_info_str}"
    return system_info


# Function to get server status information
def get_server_status():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram_info = psutil.virtual_memory()
    disk_info = psutil.disk_usage("/")
    network_info = psutil.net_io_counters()
    system_info = get_system_info()

    server_info = (
        f"IP Address: {public_ip}\n"
        f"CPU Usage: {cpu_usage:.2f}%\n"
        f"RAM Usage: {ram_info.used / (1024 ** 3):.2f} GB / {ram_info.total / (1024 ** 3):.2f} GB\n"
        f"Disk Usage: {disk_info.used / (1024 ** 3):.2f} GB / {disk_info.total / (1024 ** 3):.2f} GB\n"
        f"Upload: {network_info.bytes_sent / (1024 ** 3):.2f} GB\n"
        f"Download: {network_info.bytes_recv / (1024 ** 3):.2f} GB\n"
        f"{system_info}\n"
    )

    return server_info


public_ip = get_public_ip()


# Event handlers
@client.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    info_button = Button.inline("Info", b"info")
    help_button = Button.inline("Help", b"help")
    delete_button = Button.inline("Delete", b"delete")

    [[info_button], [delete_button]]

    start_text = f"Welcome to the server status bot! Use the /status command to get server information."
    x = await event.respond(
        start_text, buttons=[[info_button], [help_button, delete_button]]
    )
    await asyncio.sleep(5)
    await x.delete()


@client.on(events.NewMessage(pattern="/status"))
async def status_handler(event):
    server_info = get_server_status()
    refresh_button = Button.inline("Refresh", b"refresh")
    info_button = Button.inline("Info", b"info")
    help_button = Button.inline("Help", b"help")
    delete_button = Button.inline("Delete", b"delete")

    buttons = [[refresh_button, info_button], [help_button, delete_button]]

    sent_message = await event.respond(server_info, buttons=buttons)
    sent_messages[event.chat_id] = sent_message


@client.on(events.CallbackQuery())
async def callback_handler(event):
    callback_data = event.data.decode("utf-8")

    if callback_data == "refresh":
        await refresh_handler(event)
    elif callback_data == "info":
        await info_handler(event)
    elif callback_data == "delete":
        await delete_handler(event)
    elif callback_data == "help":
        await help_handler(event)


async def help_handler(event):
    help_text = (
        "This bot provides server status information. Use the following commands:\n"
    )
    help_text += "/start - Start the bot and see a welcome message\n"
    help_text += "/status - Get the current server status"

    refresh_button = Button.inline("Home", b"refresh")
    info_button = Button.inline("Info", b"info")
    delete_button = Button.inline("Delete", b"delete")

    [[refresh_button, info_button], [delete_button]]

    await event.edit(
        help_text, buttons=[[refresh_button, info_button], [delete_button]]
    )


async def refresh_handler(event):
    server_info = get_server_status()
    refresh_button = Button.inline("Refresh", b"refresh")
    info_button = Button.inline("Info", b"info")
    help_button = Button.inline("Help", b"help")
    delete_button = Button.inline("Delete", b"delete")

    current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    server_info_with_timestamp = f"{server_info}\n\nLast Refreshed: {current_timestamp}"

    await event.edit(
        server_info_with_timestamp,
        buttons=[[refresh_button, info_button], [help_button, delete_button]],
    )


async def info_handler(event):
    uname = platform.uname()
    softw = "**System Information**\n"
    softw += f"`System   : {uname.system}`\n"
    softw += f"`Release  : {uname.release}`\n"
    softw += f"`Version  : {uname.version}`\n"
    softw += f"`Machine  : {uname.machine}`\n"

    uptime = get_system_uptime()
    softw += f"`Uptime   : {uptime}`\n"

    refresh_button = Button.inline("Home", b"refresh")
    help_button = Button.inline("Help", b"help")
    delete_button = Button.inline("Delete", b"delete")

    buttons = [[refresh_button], [help_button, delete_button]]

    sent_message = await event.edit(softw, buttons=buttons)
    sent_messages[event.chat_id] = sent_message


async def delete_handler(event):
    await event.delete()


# Run the client until disconnected
client.run_until_disconnected()
