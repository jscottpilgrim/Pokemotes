from functools import partial
import re
import fullPokemonCommand
import pokemonCommand
import cfg
import validators
import libs
import time

class CurrentTime:
    def __init__(self):
        self.now = 0
    def update(self):
        self.now = int(time.time())
    def compareToNow(self):
        return int(time.time()) - self.now

validators = {
    'repeats': validators.AllowRepeats(cfg.DEFAULT_ALLOW_REPEATS),
    'userLimit': validators.UserLimit(cfg.DEFAULT_USER_LIMIT)
}

streamerName = cfg.CHAN.strip()[1:].lower()
now = CurrentTime()

acceptTwitchPlaysActions = False

#roundabout way of implementing sub only mode using streamelements bot as a middleman
#def pokemon(username, sock, queue, text):
#    if (username.lower() == streamerName) or (username.lower() == "streamelements"):
#        params = text.split()
#        un = params[0]
#        text = " ".join(params[1:])
#        #pokemonCommand.pokemonCommand(un, sock, queue, text, validators)
#        ability = 0
#        if len(params) >= 5:
#            try:
#                ability = int(params[4])
#            except:
#                outt = "Invalid. " + params[4] + " is not an integer."
#                print(outt)
#        if (ability == 25) and (username.lower() != streamerName):
#            outputText = "Wonder Guard is restricted."
#            libs.chat(sock, outputText)
#        else:
#            text = " ".join(params[1:])
#            pokemonCommand.pokemonCommand(un, sock, queue, text, validators)

def pokemon(username, sock, queue, text):
    pokemonCommand.pokemonCommand(username, sock, queue, text, validators)
    #comment the above line and uncomment the section below to restrict wonder guard to streamer only
    #params = text.split()
    #ability = 0
    #if len(params) >= 4:
    #    try:
    #        ability = int(params[3])
    #    except:
    #        outt = "Invalid. " + params[3] + " is not an integer."
    #        print(outt)
    #if (ability == 25) and (username.lower() != streamerName):
    #    outputText = "Wonder Guard is restricted."
    #    libs.chat(sock, outputText)
    #else:
    #    pokemonCommand.pokemonCommand(username, sock, queue, text, validators)

def toggleRepeats(username, sock, queue, text):
    if (username.lower() == streamerName):
        newValue = not validators['repeats'].allow
        validators['repeats'].allow = newValue
        if newValue:
            outputText = "Repeat emotes are now enabled"
        else:
            outputText = "Repeat emotes are now disabled"
        libs.chat(sock, outputText)

def userLimit(username, sock, queue, text):
    if (username.lower() == streamerName):
        try:
            validators['userLimit'].limit = int(text)
            libs.chat(sock, "Max Pokemon in queue per user has been set to " + str(text))
        except ValueError:
            libs.chat(sock, "That is not a valid integer.")


def helpCommand(username, sock, queue, text):
    if (now.compareToNow() > cfg.HELP_COOLDOWN_SECONDS):
        libs.chat(sock, "Type !pokemote (emote) or !pokemote (emote) (type1) (type2) to create a Pokemon! Any Twitch emotes or FFZ emotes will work. Type !advanced for more detail.")
        now.update()

def advancedHelp(username, sock, queue, text):
    if (now.compareToNow() > cfg.HELP_COOLDOWN_SECONDS):
        libs.chat(sock, "Advanced pokemote help: https://github.com/jscottpilgrim/Pokemotes/blob/master/advancedCommandHelp.txt")
        now.update()

def moveList(username, sock, queue, text):
    if (now.compareToNow() > cfg.HELP_COOLDOWN_SECONDS):
        libs.chat(sock, "move list: https://github.com/jscottpilgrim/Pokemotes/blob/master/moveset.csv")
        now.update()

def abilityList(username, sock, queue, text):
    if (now.compareToNow() > cfg.HELP_COOLDOWN_SECONDS):
        libs.chat(sock, "ability list: https://github.com/jscottpilgrim/Pokemotes/blob/master/abilities.csv")
        now.update()

def commandList(username, sock, queue, text):
    if (now.compareToNow() > cfg.HELP_COOLDOWN_SECONDS):
        libs.chat(sock, "pokemote command list: pokemote, pokemotehelp, movelist, abilitylist, source")
        now.update()

def sourceCode(username, sock, queue, text):
    if (now.compareToNow() > cfg.HELP_COOLDOWN_SECONDS):
        libs.chat(sock, "source: https://github.com/jscottpilgrim/Pokemotes")
        now.update()

def tpStart(username, sock, queue, text):
    if (username.lower() == streamerName):
        global acceptTwitchPlaysActions
        acceptTwitchPlaysActions = True
        libs.chat(sock, f"updated twitch plays status to {acceptTwitchPlaysActions}")

def tpStop(username, sock, queue, text):
    if (username.lower() == streamerName):
        global acceptTwitchPlaysActions
        acceptTwitchPlaysActions = False
        libs.chat(sock, f"updated twitch plays status to {acceptTwitchPlaysActions}")

def noCommand(username, sock, queue, text):
    pass
    
commands = {
    "!pokemote": pokemon,
    "!toggleRepeats": toggleRepeats,
    "!setUserLimit": userLimit,
    "!pokemotehelp": helpCommand,
    "!advanced": advancedHelp,
    "!movelist": moveList,
    "!abilitylist": abilityList,
    "!cmdlist": commandList,
    "!source": sourceCode,
    "!tpstart": tpStart,
    "!tpstop": tpStop
}

def parseTextCommand(text):
    command = re.findall("^!.*", text)
    if len(command) > 0:
        return command[0].split()[0]

def parseTextParams(text):
    splitText = text.split(' ', 1)
    if len(splitText) > 1:
        return splitText[1]

def commandFactory(text):
    tpActionCheck(text)
    return partial(commands.get(parseTextCommand(text), noCommand), text=parseTextParams(text))

def tpActionCheck(text):
    if acceptTwitchPlaysActions:
        msg = text.lower()
        if msg == 'up':
            PressAndHoldKey(UP_ARROW, 0.2)
        elif msg == 'down':
            PressAndHoldKey(DOWN_ARROW, 0.2)
        elif msg == 'left':
            PressAndHoldKey(LEFT_ARROW, 0.2)
        elif msg == 'right':
            PressAndHoldKey(RIGHT_ARROW, 0.2)
        elif msg == 'a':
            PressAndHoldKey(Z, 0.1)
        elif msg == 'b':
            PressAndHoldKey(X, 0.1)
        #elif msg == 'l':
        #    PressAndHoldKey(A, 0.1)
        #elif msg == 'r':
        #    PressAndHoldKey(S, 0.1)
        elif msg == 'select':
            PressAndHoldKey(BACKSPACE, 0.1)
        elif msg == 'start':
            PressAndHoldKey(ENTER, 0.1)

#some of doug's twitch plays code
import time
import ctypes
import pynput

SendInput = ctypes.windll.user32.SendInput

# Using DirectX key codes and input functions below.
# This DirectX code is partially sourced from: https://stackoverflow.com/questions/53643273/how-to-keep-pynput-and-ctypes-from-clashing

# Presses and permanently holds down a keyboard key
def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Releases a keyboard key if it is currently pressed down
def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

# Helper function. Holds down a key for the specified number of seconds, then releases it.
def PressAndHoldKey(hexKeyCode, seconds):
    PressKeyPynput(hexKeyCode)
    time.sleep(seconds)
    ReleaseKeyPynput(hexKeyCode)

###############################################
# DIRECTX KEY CODES
# These codes identify each key on the keyboard.
# Note that DirectX's key codes (or "scan codes") are NOT the same as Windows virtual hex key codes. 
#   DirectX codes are found at: https://docs.microsoft.com/en-us/previous-versions/visualstudio/visual-studio-6.0/aa299374(v=vs.60)
Q = 0x10
W = 0x11
E = 0x12
R = 0x13
T = 0x14
Y = 0x15
U = 0x16
I = 0x17
O = 0x18
P = 0x19
A = 0x1E
S = 0x1F
D = 0x20
F = 0x21
G = 0x22
H = 0x23
J = 0x24
K = 0x25
L = 0x26
Z = 0x2C
X = 0x2D
C = 0x2E
V = 0x2F
B = 0x30
N = 0x31
M = 0x32
ESC = 0x01
ONE = 0x02
TWO = 0x03
THREE = 0x04
FOUR = 0x05
FIVE = 0x06
SIX = 0x07
SEVEN = 0x08
EIGHT = 0x09
NINE = 0x0A
ZERO = 0x0B
MINUS = 0x0C
EQUALS = 0x0D
BACKSPACE = 0x0E
SEMICOLON = 0x27
TAB = 0x0F
CAPS = 0x3A
ENTER = 0x1C
LEFT_CONTROL = 0x1D
LEFT_ALT = 0x38
LEFT_SHIFT = 0x2A
SPACE = 0x39
DELETE = 0x53
COMMA = 0x33
PERIOD = 0x34
BACKSLASH = 0x35
NUMPAD_0 = 0x52
NUMPAD_1 = 0x4F
NUMPAD_2 = 0x50
NUMPAD_3 = 0x51
NUMPAD_4 = 0x4B
NUMPAD_5 = 0x4C
NUMPAD_6 = 0x4D
NUMPAD_7 = 0x47
NUMPAD_8 = 0x48
NUMPAD_9 = 0x49
NUMPAD_PLUS = 0x4E
NUMPAD_MINUS = 0x4A
LEFT_ARROW = 0xCB
RIGHT_ARROW = 0xCD
UP_ARROW = 0xC8
DOWN_ARROW = 0xD0
LEFT_MOUSE = 0x100
RIGHT_MOUSE = 0x101
MIDDLE_MOUSE = 0x102
MOUSE3 = 0x103
MOUSE4 = 0x104
MOUSE5 = 0x105
MOUSE6 = 0x106
MOUSE7 = 0x107
MOUSE_WHEEL_UP = 0x108
MOUSE_WHEEL_DOWN = 0x109
########################################################