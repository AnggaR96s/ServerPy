#!/bin/bash

# Check if the script is run as root
if [ "$EUID" -ne 0 ]; then
  echo "This script must be run as root."
  exit 1
fi

# Check if python3 is installed, if not, install it
if ! command -v python3 &> /dev/null; then
  echo "Installing python3..."
  apt-get update
  apt-get install -y python3
fi

# Check if pip3 is installed, if not, install it
if ! command -v pip3 &> /dev/null; then
  echo "Installing python3-pip..."
  apt-get update
  apt-get install -y python3-pip
fi

# Specify the GitHub repository URL
REPO_URL="https://github.com/AnggaR96s/ServerPy.git"

# Set the repository directory
REPO_DIR="/opt/ServerPy"

# Clone the GitHub repository
if [ ! -d "$REPO_DIR" ]; then
  git clone "$REPO_URL" "$REPO_DIR"
else
  echo "Repository already exists in $REPO_DIR."
fi

# Install required Python packages from requirements.txt
pip3 install -r "$REPO_DIR/requirements.txt"

# Set the script name to server.py
SCRIPT_NAME="server.py"

# Create the systemd service unit file
SERVICE_FILE="/etc/systemd/system/$SCRIPT_NAME.service"

cat <<EOF > "$SERVICE_FILE"
[Unit]
Description=Custom Python Script: $SCRIPT_NAME
After=network.target

[Service]
ExecStart=/usr/bin/python3 $REPO_DIR/$SCRIPT_NAME
WorkingDirectory=$REPO_DIR
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Read input for config variables
read -p "Enter your API_ID: " API_ID
read -p "Enter your API_HASH: " API_HASH
read -p "Enter your BOT_TOKEN: " BOT_TOKEN

# Write config.env file
CONFIG_FILE="$REPO_DIR/config.env"
cat <<EOF > "$CONFIG_FILE"
API_ID='$API_ID'
API_HASH='$API_HASH'
BOT_TOKEN='$BOT_TOKEN'
EOF

# Set appropriate permissions for the config.env file
chmod 600 "$CONFIG_FILE"

# Reload systemd
systemctl daemon-reload

# Enable and start the service
systemctl enable "$SCRIPT_NAME.service"
systemctl start "$SCRIPT_NAME.service"

# Print status
systemctl status "$SCRIPT_NAME.service"
