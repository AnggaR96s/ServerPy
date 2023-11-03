# 🤖 ServerPy - Server Status Telegram Bot

ServerPy is a versatile Python script that creates a Telegram bot for real-time server status monitoring and reporting. Leveraging the power of the Telethon library, this bot provides insights into CPU usage, RAM consumption, disk space utilization, network activity, and comprehensive system information. Whether you're a system administrator or simply curious about your server's performance, ServerPy has got you covered.

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/AnggaR96s/ServerPy/blob/main/LICENSE)

## 🚀 Features

- 📊 Obtain and display CPU usage, RAM usage, disk space, and network activity.
- 🖥️ Fetch and show system information such as operating system details, release, version, and machine information.
- 🔄 Refresh server status information on demand through Telegram commands.
- 📲 Utilize inline buttons for interactions within the Telegram chat.
- 👥 Only Allowed users can use this bot.
- 🎉 Full of emojis!

## 🛠️ Prerequisites

- 🐍 **Python**: Python 3.x is required to run this script.
- 📚 **Telethon**: Install the Telethon library using `pip`:

  ```bash
  pip install telethon
  ```

## 🚴 Usage

1. Clone the ServerPy repository:

   ```bash
   git clone https://github.com/AnggaR96s/ServerPy.git
   cd ServerPy
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `config.env` file and add your Telegram API credentials and bot token:

   ```env
   API_ID=your_api_id
   API_HASH=your_api_hash
   BOT_TOKEN=your_bot_token
   ALLOWED_USERS=user_id1,user_id2,user_id3
   ```

4. Run the `server.py` script:

   ```bash
   python server.py
   ```

5. Interact with the bot on Telegram.

## 🤖 Bot Commands

- `/start`: Initiate the bot and receive a welcome message. The message will be automatically removed after 5 seconds.
- `/status`: Get the latest server status, including CPU, RAM, disk, and network usage. Inline buttons are provided for refreshing, and viewing additional information.

## 📲 Inline Query
You can use inline queries to quickly access server status information. Start a message with "status" to retrieve the server status.

## 📦 Installation Script

The `install.sh` script automates the deployment process for ServerPy. It checks prerequisites, clones the repository, installs dependencies, and sets up the systemd service. Run the script with root privileges:

```bash
wget https://raw.githubusercontent.com/AnggaR96s/ServerPy/main/install.sh
chmod +x install.sh
sudo ./install.sh
```

## 🎨 Customization

The ServerPy project is designed to be highly customizable. Feel free to modify the scripts to add new features, customize messages, or enhance interactions according to your unique requirements.

## 🙌 Acknowledgements

- This project utilizes the [Telethon](https://github.com/LonamiWebs/Telethon) library for Telegram API interaction.
- Special thanks to [AnggaR96s](https://github.com/AnggaR96s) for creating the original ServerPy project.

## 📜 License

This script is provided under the MIT License. For more information, see the [LICENSE](https://github.com/AnggaR96s/ServerPy/blob/main/LICENSE) file.

---

Feel free to customize this template further to provide additional information or details specific to your use case.
