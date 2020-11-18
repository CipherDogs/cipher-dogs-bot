touch data.json
pip3 install -r requirements.txt
cp bot.service /etc/systemd/system/bot.service
systemctl start bot.service
