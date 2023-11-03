import asyncio
import logging
import requests
import platform
import psutil
from datetime import datetime, timedelta
from telethon.sync import TelegramClient, events
from telethon.tl.custom.button import Button

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Read API_ID, API_HASH, BOT_TOKEN, and ALLOWED_USERS from config.env
with open("config.env") as f:
    for line in f:
        if line.startswith("API_ID"):
            API_ID = line.strip().split("=")[1].strip().replace("'", "")
        elif line.startswith("API_HASH"):
            API_HASH = line.strip().split("=")[1].strip().replace("'", "")
        elif line.startswith("BOT_TOKEN"):
            BOT_TOKEN = line.strip().split("=")[1].strip().replace("'", "")
        elif line.startswith("ALLOWED_USERS"):
            ALLOWED_USERS = (
                line.strip().split("=")[1].strip().replace("'", "").split(",")
            )

# Handle send_message
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


def get_public_ip():
    response = requests.get("https://api64.ipify.org?format=json")
    if response.status_code == 200:
        ip_info = response.json()
        public_ip = ip_info["ip"]
        return public_ip
    else:
        return None


def get_ip_details(ip_address):
    # Get IP details using the free IPinfo.io service
    url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        return None


def get_system_info_output():
    # Get uptime info
    uptime_str = get_system_uptime()

    # Get public IP
    public_ip = get_public_ip()
    ip_details = get_ip_details(public_ip) if public_ip else None

    # Get CPU information
    cpu_usage = psutil.cpu_percent(interval=1)
    cpu_info = platform.processor()
    cpu_cores = psutil.cpu_count(logical=False)
    cpu_count = psutil.cpu_count(logical=True)
    cpu_count_str = f"{cpu_cores} physical, {cpu_count} logical"
    cpu_freq = psutil.cpu_freq().current

    # Get memory information
    memory = psutil.virtual_memory()
    total_memory = memory.total // (1024 ** 2)  # Convert to MiB

    # Get OS information
    os_info = platform.platform()
    kernel_version = platform.release()

    # Get hostname
    hostname = platform.node()

    # Get disk usage information and calculate percentage
    disk_info = psutil.disk_usage("/")
    disk_total = disk_info.total / (1024 ** 3)  # Convert to GB
    disk_used = disk_info.used / (1024 ** 3)  # Convert to GB
    disk_percent = (disk_used / disk_total) * 100  # Disk usage percentage

    # Get RAM info
    ram_info = psutil.virtual_memory()
    ram_total = ram_info.total / (1024 ** 3)  # Convert to GB
    ram_used = ram_info.used / (1024 ** 3)  # Convert to GB
    ram_percent = ram_info.percent  # RAM usage percentage

    # Get swap memory info and percentage
    swap_info = psutil.swap_memory()
    swap_total = swap_info.total / (1024 ** 3)  # Convert to GB
    swap_used = swap_info.used / (1024 ** 3)  # Convert to GB
    swap_percent = swap_info.percent  # Swap memory usage percentage

    # Function to get bandwidth information
    def get_bandwidth_info():
        net_io = psutil.net_io_counters()
        bytes_sent = net_io.bytes_sent
        bytes_received = net_io.bytes_recv
        mb_sent = bytes_sent / (1024 * 1024)
        mb_received = bytes_received / (1024 * 1024)
        return mb_sent, mb_received

    # Function to get the network status as part of system information
    def get_network_info():
        mb_sent, mb_received = get_bandwidth_info()
        network_info = f"In: {mb_received:.2f} MB / Out: {mb_sent:.2f} MB\n"
        return network_info

    # Generate the output
    network_info = get_network_info()
    output = "**System Info**\n"
    output += "**-----------**\n"
    if public_ip:
        output += f"**IP Address** `{public_ip}`\n"
        if ip_details:
            output += f"**City** `{ip_details.get('city')}`\n"
            output += f"**Region** `{ip_details.get('region')}`\n"
            output += f"**Country** `{ip_details.get('country')}`\n"
            output += f"**Location** `{ip_details.get('loc')}`\n"
        else:
            output += "Unable to retrieve IP details for the public IP.\n"
    output += f"**Processor** `{cpu_info}`\n"
    output += f"**CPU Usage** `{cpu_usage}%`\n"
    output += f"**CPU Cores** `{cpu_count_str}`\n"
    output += f"**CPU Freq** `@{cpu_freq:.3f} MHz`\n"
    output += f"**Disk Usage** `{disk_used:.2f} GB / {disk_total:.2f} GB ({disk_percent:.2f}%)`\n"
    output += f"**Memory** `{total_memory} MiB`\n"
    output += (
        f"**RAM Usage** `{ram_used:.2f} GB / {ram_total:.2f} GB ({ram_percent}%)`\n"
    )
    output += f"**Swap** `{swap_used:.2f} GB / {swap_total:.2f} GB ({swap_percent}%)`\n"
    output += f"**Network info** `{network_info}`"
    output += f"**Uptime** `{uptime_str}`\n\n"
    output += f"**OS** `{os_info}`\n"
    output += f"**Arch** `{platform.architecture()[0]} (64 Bit)`\n"
    output += f"**Kernel** `{kernel_version}`\n"
    output += f"**Hostname** `{hostname}`\n"

    return output


@client.on(events.NewMessage(pattern="/start"))
async def start_handler(event):
    if str(event.sender_id) in ALLOWED_USERS:
        info_button = Button.inline("Info", b"info")
        help_button = Button.inline("Help", b"help")
        start_text = f"Welcome to the server status bot! Use the /status command to get server information."
        x = await event.respond(start_text, buttons=[[info_button], [help_button]])
        await asyncio.sleep(30)
        await x.delete()
    else:
        user_id = event.sender_id
        await client.send_message(user_id, "You are not allowed to use this bot.")


@client.on(events.NewMessage(pattern="/status"))
async def status_handler(event):
    if str(event.sender_id) in ALLOWED_USERS:
        uptime = get_system_uptime()
        system_info_output = get_system_info_output()
        refresh_button = Button.inline("Refresh", b"refresh")
        info_button = Button.inline("Info", b"info")
        help_button = Button.inline("Help", b"help")
        buttons = [[refresh_button, info_button, help_button]]
        sent_message = await event.respond(system_info_output, buttons=buttons)
        sent_messages[event.chat_id] = sent_message
    else:
        user_id = event.sender_id
        await client.send_message(user_id, "You are not allowed to use this bot.")


@client.on(events.InlineQuery)
async def inline_query_handler(event):
    if str(event.sender_id) in ALLOWED_USERS:
        query = event.text.strip()
        if query == "status":
            uptime = get_system_uptime()
            system_info_output = get_system_info_output()
            refresh_button = Button.inline("Refresh", b"refresh")
            info_button = Button.inline("Info", b"info")
            help_button = Button.inline("Help", b"help")
            buttons = [[refresh_button, info_button, help_button]]
            result = await event.builder.article(
                title="Status Info",
                description="Show server status info.",
                text=system_info_output,
                buttons=buttons,
            )
            await event.answer([result])
        else:
            await event.answer([])  # No results for unrecognized queries
    else:
        user_id = event.sender_id
        await client.send_message(user_id, "You are not allowed to use this bot.")


@client.on(events.CallbackQuery())
async def callback_handler(event):
    callback_data = event.data.decode("utf-8")

    if callback_data == "refresh":
        await refresh_handler(event)
    elif callback_data == "info":
        await info_handler(event)
    elif callback_data == "help":
        await help_handler(event)


async def help_handler(event):
    if str(event.sender_id) in ALLOWED_USERS:
        help_text = (
            "This bot provides server status information. Use the following commands:\n"
        )
        help_text += "/start - Start the bot and see a welcome message\n"
        help_text += "/status - Get the current server status"
        refresh_button = Button.inline("Home", b"refresh")
        info_button = Button.inline("Info", b"info")

        [[refresh_button, info_button]]
        await event.edit(help_text, buttons=[[refresh_button, info_button]])
    else:
        user_id = event.sender_id
        sent_messages = {}
        await client.send_message(user_id, "You are not allowed to use this bot.")


async def refresh_handler(event):
    if str(event.sender_id) in ALLOWED_USERS:
        system_info_output = get_system_info_output()
        refresh_button = Button.inline("Refresh", b"refresh")
        info_button = Button.inline("Info", b"info")
        help_button = Button.inline("Help", b"help")

        buttons = [[refresh_button, info_button, help_button]]

        current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        server_info_with_timestamp = (
            f"{system_info_output}\n\nLast Refreshed: {current_timestamp}"
        )

        await event.edit(
            server_info_with_timestamp,
            buttons=buttons,
        )
    else:
        user_id = event.sender_id
        sent_messages = {}
        await client.send_message(user_id, "You are not allowed to use this bot.")


async def info_handler(event):
    if str(event.sender_id) in ALLOWED_USERS:
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

        buttons = [[refresh_button, help_button]]

        sent_messages = {}
        sent_message = await event.edit(softw, buttons=buttons)
        sent_messages[event.chat_id] = sent_message
    else:
        user_id = event.sender_id
        sent_messages = {}
        await client.send_message(user_id, "You are not allowed to use this bot.")


# Run the client until disconnected
client.run_until_disconnected()
