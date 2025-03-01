from src.config.utils import *
import requests

class del_all_roles:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
    
    def del_all_roles_func(self, token, guild_id):
        total = 0
        deleted = 0
        failed = 0

        Clear()
        Title("Deleting roles")
        Menu()
        print()
        Log(RED, "!", "Scraping Roles...")
        try:
            url = f"https://discord.com/api/v9/guilds/{guild_id}/roles"
            headers = { "Authorization": token }
            res = requests.get(url, headers=headers)
            if res.status_code != 200: return { "success": False, "message": "Error during scraping roles" }
            roles = res.json()
            Log(RED, "✓", "Roles successfully scraped")
        except:
            return {"success": False, "message": "Error during scraping roles"}
            
        for role in roles:
            total += 1
            try:
                url = f"https://discord.com/api/v9/guilds/{guild_id}/roles/{role["id"]}"
                headers = { "Authorization": token }
                res = requests.delete(url, headers=headers)
                if res.status_code == 204:
                    deleted += 1
                    Log(RED, "✓", f"Role {role['id']} deleted")
                elif res.status_code == 429:
                    Log(RED, "!", "Rate limit, retry after 1s")
                    time.sleep(0.96)
                    res = requests.delete(url, headers=headers)
                    if res.status_code == 204:
                        deleted += 1
                        Log(RED, "✓", f"Role {role['id']} deleted")
                    else:
                        failed += 1
                        Log(RED, "x", f"Failed to re create")
                elif res.status_code == 403:
                    failed += 1
                    Log(RED, "x", f"Missing permissions for delete {role['id']}")
                else:
                    failed += 1
                    Log(RED, "x", f"Error deleting role {role['id']}")
            except:
                failed += 1
                Log(RED, "x", f"Error while deleting role {role['id']}")
            Title(f"Deleting roles | {deleted} deleted | {failed} failed")
        
        return { "success": True, "total": total, "deleted": deleted, "failed": failed}
    
    def main(self):
        Clear()
        Title("Delete Roles")
        Menu()
        print()
        sure = Ask("Are you sure to delete all roles (y/n)").strip().lower() in ["y", "yes", "o", "oui", "true"]
        if not sure: return
        result = self.del_all_roles_func(self.token, self.guild_id)
        if not result["success"]:
            SleepLog(RED, "x", result["message"])
            return
        Log(RED, "✓", f"{result["total"]} tried in total | {GREEN}{result["deleted"]}{WHITE} deleted | {RED}{result["failed"]}{WHITE} failed", wp=True)
        input()