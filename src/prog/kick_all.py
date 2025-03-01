from src.config.utils import *
import requests

class kick_all:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
    
    def kick_all_func(self, token, guild_id):
        total = 0
        kicked = 0
        failed = 0

        Clear()
        Title("Kicking members")
        Menu()
        print()
        Log(RED, "!", "Scraping members...")
    
    def main(self):
        Clear()
        Title("Kick All")
        Menu()
        print()
        sure = Ask("Are you sure to kick all members (y/n)").strip().lower() in ["y", "yes", "o", "oui", "true"]
        if not sure: return
        result = self.kick_all_func(self.token, self.guild_id)