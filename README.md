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


Some ChatGPT convo logs:
https://chatgpt.com/c/67d759bc-2038-8011-a9d1-8589fc7145dc

