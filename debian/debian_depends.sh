#!/bin/bash
#
#


printf "Install sudo\t\t\t"
apt-get -yfq install sudo 2>&1 1>>/dev/null && echo "[OK]" || echo "[ERROR]"
printf "Install python3-full\t\t"
sudo apt-get -yfq install python3-full 2>&1 1>>/dev/null && echo "[OK]" || echo "[ERROR]"
printf "Install python3-pip\t\t"
sudo apt-get -yfq install python3-pip 2>&1 1>>/dev/null && echo "[OK]" || echo "[ERROR]"
printf "Install golang\t\t\t"
sudo apt-get -yfq install golang 2>&1 1>>/dev/null && echo "[OK]" || echo "[ERROR]"

printf "Install pip requirements.txt\t"
#sudo pip install --break-system-packages --no-color --no-python-version-warning --root-user-action=ignore -r requirements.txt 1>&2 2>&1  1>>/dev/null && echo "[OK]" || echo "[ERROR]"
sudo python3 -m venv
