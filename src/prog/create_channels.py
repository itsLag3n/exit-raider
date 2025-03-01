from src.config.utils import *
import requests
import random

class create_channels:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.name_channels = None
        self.number_channels = None
    
    def create_text_channels_func(self, token, guild_id, name_channels, num_channels):
        total = 0
        created = 0
        failed = 0
        alphabet_digit = "abcdefghijklmnopqrstuvwxyz0123456789"

        Clear()
        Title("Creating Channels")
        Menu()
        print()
        randomize = not name_channels
        for i in range(num_channels):
            total += 1
            if randomize: name_channels = "".join(random.sample(alphabet_digit, 36))
            try:
                url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
                headers = { "Authorization": token }
                payload = { "name": name_channels, "type": 0 }
                res = requests.post(url, headers=headers, json=payload)
                if res.status_code == 201:
                    created += 1
                    Log(RED, "✓", f"Channel {res.json()["id"]} created")
                elif res.status_code == 429:
                    Log(RED, "!", "Rate limit, retry after 1s")
                    time.sleep(0.96)
                    res = requests.delete(url, headers=headers, json=payload)
                    if res.status_code == 204:
                        deleted += 1
                        Log(RED, "✓", f"Channel {res.json()["id"]} created")
                    else:
                        failed += 1
                        Log(RED, "x", f"Failed to re create")
                else:
                    failed += 1
                    Log(RED, "x", f"Error creating a channel")
            except:
                failed += 1
                Log(RED, "x", f"Error creating a channel")
            Title(f"Deleting roles | {created} created | {failed} failed")
        
        return { "success": True, "total": total, "created": created, "failed": failed }
    
    def main(self):
        Clear()
        Title("Create Channels")
        Menu()
        print()
        self.name_channels = Ask("Enter channels name (leave blank for random names)").strip()
        self.number_channels = Ask("Enter number of channels to create").strip()
        if not self.number_channels.isdigit() or int(self.number_channels) <= 0:
            SleepLog(RED, "x", "Invalid number of channels", wp=True)
            return
        result = self.create_text_channels_func(self.token, self.guild_id, self.name_channels, int(self.number_channels))
        if result["success"]:
            Log(RED, "✓", f"{result["total"]} tried in total | {GREEN}{result["created"]}{WHITE} created | {RED}{result["failed"]}{WHITE} failed", wp=True)
        input()