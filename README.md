## Start using WADB



- This guide is for Debian 10

- Create an bot on [Discord dev page](https://discord.com/developers/applications) and save the bot token.

- For now, it only works with Alpha-core



## Install guide



```Bash
# dependencies
apt install python3 tmux

# Python3 dependencies
pip3 install virtualenv virtualenvwrapper

cd /opt

# download repository
git clone https://github.com/diff3/wadb

# create home dir and create user, give it a proper password!
adduser --home /opt/wadb wadb

cd /opt/wadb

# database. Change password in the SQL file before running it!
mysql -u root -p < /opt/wadb/etc/db-setup.sql

# Python virtualenv
mkvirtualenv wadb
pip3 install -r requirements.txt

# env
cp etc/env.dist .env

# edit the .env file and att your credentials.
# also add the token you got from [Discord dev page]
# you can now start wadb by typing

chown wadb:wadb -R /opt/wadb

workin wadb # if needed
python3 main.py
```



### Service



```Bash
# install wadb.service and start it.
cp etc/wadb.service /etc/systemd/system
systemctl daemon-reload
systemctl enable wadb
systemctl start wadb
```

Now you are done, below is just extra information.

### Tmux



Tmux is a program to create virtualshell. If your using a server you can log into the server and create a tmux shell, start compile and exit. Later you just log into your virtual shell again.



Everything with tmux is handlet by short commands. For most beginner commands it start's with ctrl+b (c-b)

- the only command you need to know is. c-b d - detach window. So you don't kill you running script.



```bash
# to create a new session
tmux

# create a session and name it.
tmux new -s "HelloWorld"

# attach to a session
tmux a -t "0" # if you fogot to name it.
tmux a -t "HelloWorld"

tmux ls # list active sessions

# to exit and kill the session
exit
```



#### Check you running bot (service)



First we need to log into wadb account and then we attach to a tmux session

```bash
su wadb
tmux a -t "wadb"

# to detach type
c-b d
```





## Assets

### database

```sql
/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

CREATE DATABASE wadb;
USE wadb;

DROP TABLE IF EXISTS `discord`;
CREATE TABLE `discord` (
  `id` bigint(20) unsigned NOT NULL AUTO_INCREMENT,
  `account` varchar(256) NOT NULL,
  `discord_id` varchar(256) NOT NULL,
  `emulator` varchar(256) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

CREATE USER 'wadb'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `alpha_%`.* TO 'wadb'@'localhost';
GRANT ALL PRIVILEGES ON `wadb%`.* TO 'wadb'@'localhost';
FLUSH PRIVILEGES;
```



### service file

```Bash
[Unit]
Description=WADB discord bot for World of Warcraft emulators
After=network.target

[Install]
WantedBy=multi-user.target

[Service]
RemainAfterExit=yes
WorkingDirectory=/opt/wadb
User=wadb
Group=wadb

ExecStart=/usr/bin/tmux new -d -s "wadb" "/opt/virtualenvs/wadb/bin/python3 main.py"
ExecStop=/usr/bin/tmux send -t wadb 'Shuting down wadb' C-m

# SECURITY
PrivateUsers=true
ProtectSystem=full
ProtectHome=true
ProtectKernelTunables=true
ProtectControlGroups=true

Restart=on-failure
RestartSec=60s
```
