# Discord Voice Channel Curfew
Automatically locks and unlocks a Discord voice channel at specific times, sending prior warning to a text channel. 

Made for a friends specific use-case, not intended to be ran by others.  
Only works in one server at a time.

Quick setup:
Required: pipenv (usually `sudo apt install pipenv`)
```bash
git clone https://github.com/Erisa/discord-voice-curfew 
cd discord-voice-curfew
pipenv install
cp config.example.py config.py
# edit config.py at this point
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
