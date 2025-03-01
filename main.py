from src.config.config import *
import requests
import json

options = {
    "!": lambda: sys.exit(),
    ">": lambda: next_page(page).main(),
    "<": lambda: previous_page(page).main(),
    "?": lambda: help_info().main(),
    "1": lambda: del_all_channels(get_token(), get_guild_id()).main(),
    "2": lambda: create_channels(get_token(), get_guild_id()).main(),
    "3": lambda: del_all_roles(get_token(), get_guild_id()).main(),
    "4": lambda: create_roles(get_token(), get_guild_id()).main(),
    "5": lambda: spammer(get_token(), get_guild_id()).main(),
    
    "!!": lambda: sys.exit(),
    ">>": lambda: next_page(page).main(),
    "<<": lambda: previous_page(page).main(),
    "??": lambda: help_info().main(),
    "01": lambda: del_all_channels(get_token(), get_guild_id()).main(),
    "02": lambda: create_channels(get_token(), get_guild_id()).main(),
    "03": lambda: del_all_roles(get_token(), get_guild_id()).main(),
    "04": lambda: create_roles(get_token(), get_guild_id()).main(),
    "05": lambda: spammer(get_token(), get_guild_id()).main(),
}

def main():
    global token, guild_id, page
    with open("config.json", "r") as f:
        config = json.load(f)
    Clear()
    Title("Put token")
    Menu()
    print()
    token = Ask("Token (leave blank to pick from config)").strip()
    if not token: token = config.get("token", "")
    try:
        r = requests.get("https://discord.com/api/v9/users/@me", headers={'Authorization': token})
        if r.status_code != 200:
            SleepLog(RED, "x", "Token Invalid", wp=True)
            sys.exit()
        set_token(token)
    except Exception:
        SleepLog(RED, "x", "Error while checking token, verify your internet connection", wp=True)
        sys.exit()
    guild_id = Ask("Guild ID (leave blank to pick from config)").strip()
    if not guild_id: guild_id = config.get("guild_id", "")
    try:
        r = requests.get(f"https://discord.com/api/v9/guilds/{guild_id}/channels", headers={'Authorization': token})
        if r.status_code == 200:
            pass
        elif r.status_code == 403:
            SleepLog(RED, "x", "Token is not in guild", wp=True)
            sys.exit()
        else:
            SleepLog(RED, "x", "Unknown Guild", wp=True)
            sys.exit()
        set_guild_id(guild_id)
    except Exception:
        SleepLog(RED, "x", "Error while checking if token is in guild, verify your internet connection", wp=True)
        sys.exit()
    while 1:
        Clear()
        Title("Menu")
        Menu(page)
        print()
        choice = Ask("Choice").strip()
        try:
            result = options[choice]()
            if not result: continue
            if result[0] == "page":
                page = result[1]
        except Exception as e:
            print("err:")
            input(e)
            InvalidChoice()

main()