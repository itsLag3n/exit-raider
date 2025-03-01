import os
import sys, ctypes
from datetime import datetime
import time

name = "Exit"
version = "1.0.0"

RESET = "\033[0m"
WHITE = "\033[37m"
GREEN = "\033[32m"
BLACK_RED = "\033[38;5;88m"
RED = "\033[31m"
GREY = "\033[90m"

page = 1
token = None
guild_id = None

def center(var: str, space: int = None):
    if not space:
        space = (os.get_terminal_size().columns - len(var.splitlines()[int(len(var.splitlines())/2)])) / 2
    
    return "\n".join((' ' * int(space)) + var for var in var.splitlines())

banner = f"""
███████╗██╗  ██╗██╗████████╗
██╔════╝╚██╗██╔╝██║╚══██╔══╝
█████╗   ╚███╔╝ ██║   ██║   
██╔══╝   ██╔██╗ ██║   ██║   
███████╗██╔╝ ██╗██║   ██║   
╚══════╝╚═╝  ╚═╝╚═╝   ╚═╝   {RESET}"""

options1 = f"""
[!!] Exit                         [>>] Next Page                    [??] Help
[01] Delete All Channels          [05] Spammer                      [09] Soon
[02] Create Channels              [06] Soon                         [10] Soon
[03] Delete All Roles             [07] Soon                         [11] Soon
[04] Create Roles                 [08] Soon                         [12] Soon
"""

options2 = f"""
[!!] Exit                         [>>] Previous Page                [??] Help
"""

def Menu(page = None):
    print(center(banner).replace("█", f"{RED}█{GREY}"))
    if page == 1:
        print(center(options1).replace("[", f"{RED}[{WHITE}").replace("]", f"{RED}]{WHITE}"))
    elif page == 2:
        print(center(options2).replace("[", f"{RED}[{WHITE}").replace("]", f"{RED}]{WHITE}"))

def Clear():
    os.system('cls' if os.name=='nt' else 'clear')

def Title(title: str):
    if sys.platform.startswith("win"):
        ctypes.windll.kernel32.SetConsoleTitleW(f"{name} v{version} | {title}")
    elif sys.platform.startswith("linux"):
        sys.stdout.write(f"\x1b]2;{name} v{version} | {title}\x07")

def Log(color, symbole, message, end="\n", flush=False, wp=False):
    if wp: print("")
    print(f"{RESET}{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} {color}[{WHITE}{symbole}{color}]{WHITE} {message}", end=end, flush=flush)

def SleepLog(color, symbole, message, end="\n", flush=False, wp=False, timee=1.5):
    Log(color, symbole, message, end, flush, wp)
    time.sleep(timee)

def Ask(text: str):
    return input(f"{RED}{text}{WHITE} > {RESET}")

def Pause():
    os.system('pause')

def CommingSoon(wp=True):
    if wp: print("")
    Log(RED, "!", "Comming Soon")
    time.sleep(1)

def InvalidChoice(wp=True):
    if wp: print("")
    Log(RED, "x", "Invalid Choice")
    time.sleep(1)

def set_token(t):
    global token
    token = t

def get_token():
    global token
    return token

def set_guild_id(g):
    global guild_id
    guild_id = g

def get_guild_id():
    global guild_id
    return guild_id
