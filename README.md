# bot-ping-server

Bot that allows monitoring of multiple servers and sends a message once it detects that a server is down. Additionally, the bot enables subscription from multiple users.

## Configuration

First, you need to create a configuration file in your project directory (you should specify the folder name). Here's a template for your configuration file:

\```json
{
    "bot_token": "111111:xxxxxxx",
    "ip_list": [
        "xxx.xxx.xxx.xxx", 
        "yyy.yyy.yyy.yyy"
    ]
}
\```

Replace `"111111:xxxxxxx"` with your actual Telegram bot token and `"xxx.xxx.xxx.xxx"`, `"yyy.yyy.yyy.yyy"` with the IP addresses of the servers you wish to monitor.

## Systemctl Service

To keep the bot running, you need to create a service in systemctl. Follow the steps below:

1. Create a new service file in the `/etc/systemd/system/` directory (e.g., `bot-ping-server.service`).
2. Add the following content to this service file:

\```ini
[Unit]
Description=Bot Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/bot-ping-server/
ExecStart=/usr/bin/python3 /home/ubuntu/bot-ping-server/bot.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
\```

3. Reload systemd, enable, and start the service with the following commands:

\```sh
sudo systemctl daemon-reload
sudo systemctl enable bot-ping-server.service
sudo systemctl start bot-ping-server.service
\```

## Interaction

After setting up, you can talk to the bot on Telegram. Use the `/subscribe` command to start receiving alerts.

Please replace all the placeholders with actual data relevant to your project. The placeholder fields might include paths, usernames, file names, IP addresses, and tokens.
 
## License
Distributed under the XYZ License. See LICENSE for more information.

## Contact
Edgar Florez - edgarfra6@gmail.com

