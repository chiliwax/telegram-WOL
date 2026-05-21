# telegram-WOL

A Telegram bot that sends Wake-on-LAN (WOL) magic packets to wake up your computers remotely and check their online status via ARP scanning.

## Features

- **Wake-on-LAN**: Send WOL magic packets to wake up your PC or macOS device
- **Status Monitoring**: Check if your devices are online using ARP network scanning
- **Multi-Device Support**: Configure and manage both Windows PC and macOS devices
- **Authorized Access**: Restrict bot access to a specific Telegram channel/chat
- **Connection Verification**: Automatically verify if the device woke up successfully with retry logic
- **Docker Support**: Easy deployment with Docker Compose

## Commands

| Command | Description |
|---------|-------------|
| `/poweron` | Wake up the configured PC |
| `/status` | Check if the PC is online |
| `/poweronmac` | Wake up the configured macOS device |
| `/statusmac` | Check if the macOS device is online |
| `/kill` | Stop the bot |

## Prerequisites

- Python 3.9+
- A Telegram Bot Token (get one from [@BotFather](https://t.me/BotFather))
- Target devices configured for Wake-on-LAN in BIOS/UEFI
- Network access to the target devices (same network or properly configured routing)
- Docker and Docker Compose (optional, for containerized deployment)

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd telegram-WOL
```

2. Create a virtual environment and install dependencies:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Create a `.env` file with your configuration:
```env
BOT_NAME=MyWOLBot
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_AUTHAURIZE_CHANNEL=your_channel_id
PC_MAC_ADDR=00:11:22:33:44:55
MACOS_MAC_ADDR=00:11:22:33:44:66
IP_RANGE=192.168.1.0/24
RECONNECTION_ATEMPT=5
```

4. Run the bot:
```bash
python main.py
```

### Docker Deployment

1. Build and run with Docker Compose:
```bash
docker-compose up -d
```

**Note**: The `docker-compose.yml` uses `network_mode: host` to allow ARP scanning on the host network.

## Configuration

| Variable | Description | Example |
|----------|-------------|---------|
| `BOT_NAME` | Name of your bot | `MyWOLBot` |
| `TELEGRAM_BOT_TOKEN` | Token from @BotFather | `1234567890:ABCdefGHIjklMNOpqrSTUvwxyz` |
| `TELEGRAM_AUTHAURIZE_CHANNEL` | Telegram chat ID allowed to use the bot | `-1001234567890` |
| `PC_MAC_ADDR` | MAC address of your Windows/Linux PC | `00:11:22:33:44:55` |
| `MACOS_MAC_ADDR` | MAC address of your macOS device | `00:11:22:33:44:66` |
| `IP_RANGE` | Network range for ARP scanning | `192.168.1.0/24` |
| `RECONNECTION_ATEMPT` | Number of retry attempts after WOL | `5` |

### Getting Your Telegram Chat ID

1. Start a chat with your bot
2. Send any message
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Look for `"chat":{"id":` in the response

## How It Works

1. **Wake-on-LAN**: The bot uses the `wakeonlan` library to send magic packets to the target MAC address
2. **ARP Scanning**: Uses `scapy` to perform ARP requests on the configured IP range to detect if the device is online
3. **Status Check**: Compares discovered MAC addresses with configured ones to determine device status
4. **Retry Logic**: After sending WOL, the bot waits and retries to check if the device came online

## Requirements

```
asyncio
python-dotenv
python-telegram-bot
wakeonlan
scapy
```

## Troubleshooting

### Device doesn't wake up
- Ensure Wake-on-LAN is enabled in BIOS/UEFI settings
- Check that the device is connected via Ethernet (WOL often doesn't work over Wi-Fi)
- Verify MAC address is correct
- Ensure the bot is on the same network segment as the target device

### ARP scanning not finding devices
- Verify `IP_RANGE` matches your network configuration
- Run with sufficient privileges (ARP scanning may require root/administrator)
- Check if firewall rules are blocking ARP requests

### Docker issues
- Ensure Docker has network access (uses `network_mode: host`)
- On macOS Docker Desktop, host networking may have limitations
- Try running with `--privileged` flag if ARP scanning fails

## Security Notes

- Keep your `.env` file secure and never commit it to version control
- Use a dedicated Telegram channel/group for bot access control
- Consider running the bot on a VPN if accessing devices remotely

## License

[Add your license here]

## Contributing

[Add contribution guidelines if applicable]
