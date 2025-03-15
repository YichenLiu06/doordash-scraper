# doordash-scraping

Instructions for running (Linux):

Create a .env file in the root folder with the contents:
```
API_KEY = "YOUR SCRAPYBARA API KEY HERE" 
```

Then, in a new terminal, run:
```
rye sync
. .venv/bin/activate
chmod -R +x .
python3 src/doordash-scraping/main.py
```


