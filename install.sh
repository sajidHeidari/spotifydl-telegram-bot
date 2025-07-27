#!/bin/bash

# --- Spotify Downloader Bot Installer ---
# This script automates the entire setup process.

# Define colors for better user experience
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}Welcome to the Spotify Downloader Bot Installer!${NC}"

# --- Step 1: Get API Keys from the User ---
echo -e "\n${YELLOW}I need your API keys to set up the bot.${NC}"

read -p "Enter your Telegram Bot Token: " TELEGRAM_TOKEN
read -p "Enter your Spotify Client ID: " SPOTIFY_CLIENT_ID
read -p "Enter your Spotify Client Secret: " SPOTIFY_CLIENT_SECRET

# --- Step 2: Create the .env file with the secrets ---
echo -e "\n${YELLOW}Creating the .env file with your keys...${NC}"
# Using cat with EOF to write multiline content to a file
cat > .env << EOL
# API Keys for the bot. This file is not tracked by Git.
TELEGRAM_TOKEN="${TELEGRAM_TOKEN}"
SPOTIFY_CLIENT_ID="${SPOTIFY_CLIENT_ID}"
SPOTIFY_CLIENT_SECRET="${SPOTIFY_CLIENT_SECRET}"
EOL
echo -e "${GREEN}.env file created successfully!${NC}"

# --- Step 3: Set up Python Environment ---
echo -e "\n${YELLOW}Setting up Python virtual environment...${NC}"
python3 -m venv venv

echo -e "${YELLOW}Installing required Python packages from requirements.txt...${NC}"
# Activate venv, install packages, then deactivate
source venv/bin/activate
pip install -r requirements.txt
deactivate
echo -e "${GREEN}Python environment is ready!${NC}"

# --- Step 4: Create and Start the systemd Service ---
echo -e "\n${YELLOW}Setting up the bot to run as a 24/7 service...${NC}"
# Get the absolute path to the project directory
BOT_PATH=$(pwd)
# Get the current username
USERNAME=$(whoami)
# Define the service file path
SERVICE_FILE="/etc/systemd/system/spotifydlbot.service"

# Create the service file using sudo and a heredoc
sudo bash -c "cat > ${SERVICE_FILE}" << EOL
[Unit]
Description=Telegram Spotify Downloader Bot
After=network.target

[Service]
User=${USERNAME}
WorkingDirectory=${BOT_PATH}
ExecStart=${BOT_PATH}/venv/bin/python3 ${BOT_PATH}/main.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

echo -e "${YELLOW}Reloading systemd, enabling and starting the service...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable spotifydlbot.service
sudo systemctl start spotifydlbot.service

# --- Final Confirmation ---
echo -e "\n${GREEN}====================================================="
echo -e "      🎉 Installation Complete! Your bot is now live. 🎉"
echo -e "=====================================================${NC}"
echo -e "You can check the bot's status with the command:"
echo -e "${YELLOW}sudo systemctl status spotifydlbot.service${NC}"
echo -e "\nTo see the live logs for troubleshooting, use:"
echo -e "${YELLOW}sudo journalctl -u spotifydlbot.service -f${NC}"
