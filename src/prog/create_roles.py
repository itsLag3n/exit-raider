from src.config.utils import *
import requests
import random

class create_roles:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.name_roles = None
        self.number_roles = None
    
    def create_roles_func(self, token, guild_id, name_roles, num_roles):
        total = 0
        created = 0
        failed = 0
        alphabet_digit = "abcdefghijklmnopqrstuvwxyz0123456789"

        Clear()
        Title("Creating Roles")
        Menu()
        print()
        randomize = not name_roles

        for i in range(num_roles):
            total += 1
            if randomize: name_roles = "".join(random.sample(alphabet_digit, 36))
            try:
                url = f"https://discord.com/api/v9/guilds/{guild_id}/roles"
                headers = { "Authorization": token }
                payload = { "name": name_roles, "color": random.choice([16711680, 16775936, 1834752, 65441, 57599, 4095, 8126719, 15401215]) }
                res = requests.post(url, headers=headers, json=payload)
                if res.status_code == 200:
                    created += 1
                    Log(RED, "✓", f"Role {res.json()["id"]} created")
                elif res.status_code == 429:
                    Log(RED, "!", "Rate limit, retry after 1s")
                    time.sleep(0.96)
                    res = requests.delete(url, headers=headers, json=payload)
                    if res.status_code == 204:
                        deleted += 1
                        Log(RED, "✓", f"Role {res.json()["id"]} created")
                    else:
                        failed += 1
                        Log(RED, "x", f"Failed to re create")
                else:
                    failed += 1
                    Log(RED, "x", f"Error creating a role")
            except Exception:
                failed += 1
                Log(RED, "x", f"Error creating a role")
            Title(f"Creating roles | {created} created | {failed} failed")
        
        return { "success": True, "total": total, "created": created, "failed": failed }
    
    def main(self):
        Clear()
        Title("Create Roles")
        Menu()
        print()
        self.name_roles = Ask("Roles names (leave blank for random names)")
        self.number_roles = Ask("Number of roles")
        if not self.number_roles.isdigit() or int(self.number_roles) <= 0:
            SleepLog(RED, "x", "Invalid number of roles", wp=True)
            return
        result = self.create_roles_func(self.token, self.guild_id, self.name_roles, int(self.number_roles))
        if result["success"]:
            Log(RED, "✓", f"{result["total"]} tried in total | {GREEN}{result["created"]}{WHITE} created | {RED}{result["failed"]}{WHITE} failed", wp=True)
        input()