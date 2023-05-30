# SoDA Roster Approval Script
Selenium script that runs headless (no GUI environment required).
Auto-accepts prospective members on SoDA's SunDevilSync (Campus Labs Engage) Organization.

## Dependencies
- [selenium](https://pypi.org/project/selenium/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) 
- [Google Chrome](https://www.google.com/chrome)
> Google Chrome and ChromeDriver versions need to match

## Setup Instructions:
Only tested with WSL2/Ubuntu and Ubuntu 20.04 (LTS), these instructions should work for any Debian-based OS.

Chrome can be installed with:
```bash
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install ./google-chrome-stable_current_amd64.deb
```

ChromeDriver setup (not necessary as it will be installed automatically if not detected, just improves load time slightly):
```bash
# Move chromedriver into PATH
sudo mv chromedriver /usr/local/bin
# Make it executable
sudo chmod +x /usr/local/bin/chromedriver
```

You can optionally put your login credentials in a .env file in the same directory as the script:
```bash
username=bgood
password=P@s5w0rd
```
Obviously, don't do this on a machine other people might have access to.

## Running the script
```bash
python3 engage-roster-approver.py
```
> Add `-v` arg for debug messages (e.g. when page refreshes are occurring)