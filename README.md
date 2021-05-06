# PokEmotes
Pokemon FireRed rom hack that introduces twitch integration: viewers create their own pokemon which are encountered in game, live.

# Setup Instructions
1. Download this repo as a zip
2. Download [python 3](https://www.python.org/downloads/) (make sure to check the option "add to system variables")
3. Set up config file:
   1. Log into your bot's account (if you don't have an account for your bot, you can either create one or just use your own account).
   2. Generate an [OAuth token](http://twitchapps.com/tmi/) for your bot
   3. Open twitchBot\cfg.cfg
   4. Change the value of NICK to your bot's name (in lowercase)
   5. Change the value of PASS to the OAuth token that was generated (including "oauth:")
   6. Change the value of CHAN to "#" followed by the channel you wish to join (in lowercase). For example, if you wish to join the channel "TwitchChannel", you would change this value to "#twitchchannel"
4. Run DoomRed\setupBot.bat (double click on it)
5. Download [VBA-RR](http://tasvideos.org/EmulatorResources/VBA.html)
6. Obtain a ROM of Pokemon FireRed US V1.1

# Updating Emotes
To update the cache of FFZ emote mappings, double click updateFFZ.bat, or run python twitchBot/updateFFZ.py
Updating the cache for Twitch emotes is a little more complicated. Because there are so many, updateTwitch.py saves emotes in batches of 1 million. Use combineJsonFiles.py to combine these parts, then rename combined.json to emotes.json
 - Currently the complete emote file is too large for github. The part files (as of 2021/03/24) are included in the twitchBot/emoteBackups folder

# Other Configurations
In twitchBot\cfg.cfg there are other configurations that can be set related to the gameplay itself:
- DEFAULT_USER_LIMIT: this the the maximum number of pokemon that a user can have queued at any given time. Set to 0 for no limit.
- DEFAULT_ALLOW_REPEATS: this tells the game whether or not multiple of the same emote can be queued at the same time.
- HELP_COOLDOWN_SECONDS: the cooldown time for the help command in seconds (if multiple help commands are given within this time frame, the latter responses will not be displayed)

# How to Play
## How to Run the Game
1. Run runBot.bat (double click on it)
2. Run VBA-RR and load the ROM
3. Click Tools -> Lua Scripting -> New Lua Script Window...
4. In the new window that pops up, click Browse...
5. Open lua\DoomRed.lua
6. Click Run

## Once in Game
### Playing
- Each Pokemon that is encountered (wild or during a trainer battle) will be created using from the commands that chat gives (described below). The Pokemon are entered into a queue as they are entered.

### Saving Changed Pokemon
Emote Pokemon details are saved into lua/savedChanges.lua at the start of each battle (this save includes pokemon changed in that battle.)
Upon starting the DoomRed.lua script in VBA-RR, pokemon in the party will be restored to their emote versions. If you are saving/loading via savestates, load the savestate before running the script.
The data for pokemon stored in the box is not stored in a static location. The first and second pokemon stored in box1 must be kept track of manually in order to retain their changes on reload. At the start of each battle, the lua script window will print out 6 lines of numbers (6 lua tables) each within curly braces. These correspond to the pokemon in your party. Copy one of those groups of numbers into lua/savedFirstBox.lua and another into lua/savedFirstBox2.lua then deposit the corresponding party pokemon into the first and second positions of box1. Eg. if you want to deposit the second pokemon from your party into the box, copy the second group of numbers from the lua window.

### Commands
- The following commands will add a Pokemon to the queue that looks like the given emote. The options with "type" will give the pokemon that type (case insensitive). Most other stats of the Pokemon are random:
  - !pokemon [emote]
  - !pokemon [emote] [type1]
  - !pokemon [emote] [type1] [type2]
  - !pokemon [emote] [type1] [type2] [ability] [attack1] [attack2] [attack3] [attack4]

- The following command gives a brief explanation of how to play:
  - !help

- Additional help commands:
  - !advanced
  - !movelist
  - !abilitylist
  - !cmdlist
  - !source

- The following commands are streamer only configuration commands:
  - !setUserLimit [number]
    - Sets the value of USER_LIMIT (explained above)
  - !toggleRepeats
    - Flips the value of ALLOW_REPEATS (explained above)

### TwitchPlaysPokemon
- Use these commands to enable/disable 'Twitch Plays' mode where chat can control the game via text in chat (a, b, left, right, up, down, start, select)
  - !tpstart
  - !tpstop

### Gotchas
- Gifted Pokemon have not been implemented. That means that your first Pokemon will be a regular Pokemon.
- Gamegets glitchy sometimes graphically.
- Emotes sometimes evolve into other emotes or pokemon. Bug or feature? You decide!

# Troubleshooting
- If double clicking on any of the python scripts doesn't work, try the following:
  - Open a command prompt (type "cmd" into the start menu and click enter)
  - type the following into the command prompt and hit enter:
    - cd "path/to/script"
  - type the following into the command prompt and hit enter:
    - python name_of_script.py
- To check if you have the correct version of python running:
  - type the following into a command prompt:
    - python -V
  - the output should say:
    - Python 3.6.0
