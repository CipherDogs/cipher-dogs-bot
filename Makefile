.PHONY: install
install:
	pip3 install -r requirements.txt
	cp bot.service /etc/systemd/system/bot.service
	systemctl daemon-reload

.PHONY: restart
restart:
	systemctl stop bot.service
	systemctl start bot.service

.PHONY: status
status:
	systemctl status bot.service

.PHONY: stop
stop:
	systemctl stop bot.service

.PHONY: pull
stop:
	git pull