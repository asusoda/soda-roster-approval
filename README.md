# Dependencies
- [selenium](https://pypi.org/project/selenium/)
- [python-dotenv](https://pypi.org/project/python-dotenv/)
- [ChromeDriver](https://chromedriver.chromium.org/downloads) 
- [Google Chrome](https://www.google.com/chrome)
> Google Chrome and ChromeDriver versions need to match

## Setup Instructions (WSL/Ubuntu):
Chrome can alternatively be installed with:
```bash
sudo apt install google-chrome-stable
```

```bash
# Move chromedriver into PATH
sudo mv chromedriver /usr/local/bin
# Make it executable
sudo chmod +x /usr/local/bin/chromedriver
```