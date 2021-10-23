# Trivia Discord
### Powered by [Trivia Core](https://github.com/nineclicks/trivia_core)

Discord bot should have permissions:
- Send Messages
- Read Message History
- Add Reactions

And intent:
- Server Members Intent

```bash
pip install -r requirements.txt
cp config-example.json config.json
# Add bot token, admin id, trivia channel to config.json
python trivia_discord.py
```

Trivia questions can be scraped with trivia-core `scrape.py`
