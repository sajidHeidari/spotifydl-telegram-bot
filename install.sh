#!/bin/bash

# --- Final Automated Installer for Spotify Telegram Bot ---

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${GREEN}Welcome to the Ultimate Spotify Downloader Bot Installer!${NC}"

# --- Step 1: Install all system dependencies (including ffmpeg) ---
echo -e "\n${YELLOW}Installing system dependencies (git, python3-pip, python3-venv, ffmpeg)...${NC}"
sudo apt-get update
sudo apt-get install -y git python3-pip python3-venv ffmpeg

# --- Step 2: Get API Keys from User ---
echo -e "\n${YELLOW}Please provide your API keys.${NC}"
read -p "Enter your Telegram Bot Token: " TELEGRAM_TOKEN
read -p "Enter your Spotify Client ID: " SPOTIFY_CLIENT_ID
read -p "Enter your Spotify Client Secret: " SPOTIFY_CLIENT_SECRET

# --- Step 3: Get YouTube Cookie from User (Optional but Recommended) ---
echo -e "\n${CYAN}To avoid being blocked by YouTube, providing a cookie is highly recommended.${NC}"
echo -e "1. Install the 'Cookie-Editor' extension in your browser."
echo -e "2. Go to youtube.com."
echo -e "3. Click the extension, select 'Export' -> 'Netscape' -> 'Copy to Clipboard'."
echo -e "Leave this blank and press Enter if you want to skip."
read -p "Paste your YouTube cookie content here: " YOUTUBE_COOKIE

# --- Step 4: Create configuration files ---
echo -e "\n${YELLOW}Creating configuration files (.env and cookies.txt)...${NC}"

# Create .env file
cat > .env << EOL
# API Keys for the bot
TELEGRAM_TOKEN="${TELEGRAM_TOKEN}"
SPOTIFY_CLIENT_ID="${SPOTIFY_CLIENT_ID}"
SPOTIFY_CLIENT_SECRET="${SPOTIFY_CLIENT_SECRET}"
PROXY_URL=""
EOL

# Create cookies.txt if content was provided
if [ -n "$YOUTUBE_COOKIE" ]; then
    echo "$YOUTUBE_COOKIE" > cookies.txt
    echo -e "${GREEN}cookies.txt file created successfully!${NC}"
else
    echo -e "${YELLOW}Skipping cookie file creation.${NC}"
fi

# --- Step 5: Setup Python Environment ---
echo -e "\n${YELLOW}Setting up Python virtual environment and installing packages...${NC}"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
deactivate
echo -e "${GREEN}Python environment is ready!${NC}"

# --- Step 6: Create and Start systemd Service ---
echo -e "\n${YELLOW}Setting up the bot to run as a 24/7 service...${NC}"
BOT_PATH=$(pwd)
USERNAME=$(whoami)
SERVICE_FILE="/etc/systemd/system/spotifydlbot.service"

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

sudo systemctl daemon-reload
sudo systemctl enable spotifydlbot.service
sudo systemctl start spotifydlbot.service

# --- Final Step: Show Status ---
echo -e "\n${GREEN}====================================================="
echo -e "      🎉 Installation Complete! Your bot is now live. 🎉"
echo -e "=====================================================${NC}"
echo -e "To check the bot's status, use: ${YELLOW}sudo systemctl status spotifydlbot.service${NC}"
echo -e "To view live logs, use: ${YELLOW}sudo journalctl -u spotifydlbot.service -f${NC}"
