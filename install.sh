#! /bin/bash
apt install python3-pip
python -m pip install --upgrade pip
pip install urllib3
pip install selenium==3.141.0
pip install html5lib
pip install requests
pip install webdriver-manager
pip install tk
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
sudo apt-get update
sudo apt install google-chrome-stable -y
