# Tournament Bikepolo Application
Hey Bikepolo Community,
this software is designed to help organizers schedule single player tournaments. With this tool, you can easily create schedules, manage matches, and keep track of scores and standings.

## What do I need to do get this thing?

Install python (which version?).

### Ubuntu:  (and probably Mac)

To set it up, open a terminal and type the following:

```
git clone https://github.com/edc0/tournament-maker # downloads this folder
cd tournament-maker								   # walks into the folder
pip install -r requirements.txt					   # install the list of requirements
```

### Windows:

i don't know

## Ho do I run it?

To operate, it's better to learn by doing. On the same terminal as before (i.e. from the `tournament-maker' folder), run

```
python main.py
```

and click around. Create a new tournament with the players list in "list_with_initial_rankings.csv".

## How to operate a tournament?

..



## Right, and how I set my own tournament, then?



### Old docs from [ole](https://github.com/oleuml):

1. Download the latest executable from the Releases for your system.
2. Run the `main` executable.
3. Create a new tournament
  - Add the tournament name
  - Add the player list
4. Change scoring and scheduling globally (optional):
In your app data folder the config file is located. This config file is a toml file. To edit this use an Text Editor of your choice (e.g. notepad).
The `config.toml` looks like this:
```toml
[rating]
win = 3
tie = 1
loss = 0

[mode]
mode = 'random' # or 'abc'
```
If you changed the config.toml you have to restart the application.

The app data folder is located here:
... 
5. Load tournament and start
