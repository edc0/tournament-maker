# Tournament Bikepolo Application
Hey Bikepolo Community,
this software is designed to help organizers schedule single player tournaments. With this tool, you can easily create schedules, manage matches, and keep track of scores and standings.

## How to use?
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
