cp bot.service /etc/systemd/system/bot.service
systemctl daemon-reload
systemctl stop bot.service
systemctl start bot.service
