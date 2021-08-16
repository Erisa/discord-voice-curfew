# Discord Voice Channel Curfew
Automatically locks and unlocks a Discord voice channel at specific times, sending prior warning to a text channel. 

Made for a friends specific use-case, not intended to be ran by others.  
Only works in one server at a time.

Quick setup:

```bash
# clone and cd into the repo
pipenv install
cp config.example.py config.py
# edit config.py
pipenv run python bot.py
```

or:

```bash
# clone and cd into the repo
docker build -t curfew-bot .
cp config.example.py config.py
# edit config.py
docker run --name curfew-bot -v $PWD/config.py:/usr/src/app/config.py curfew-bot
```
