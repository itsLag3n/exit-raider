from src.config.utils import *
import requests

class del_all_channels:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.del_text_channels = False
        self.del_voc_channels = False
        self.del_categories = False
    
    def del_all_channels_func(self, token, guild_id, del_text_channels, del_voc_channels, del_categories):
        total = 0
        deleted = 0
        failed = 0

        Clear()
        Title("Deleting channels")
        Menu()
        print()
        Log(RED, "!", "Scraping Channels...")
        try:
            url = f"https://discord.com/api/v9/guilds/{guild_id}/channels"
            headers = { "Authorization": token}
            response = requests.get(url, headers=headers)
            if response.status_code != 200: return { "success": False, "message": "Error during scraping channels" }
            channels = response.json()
            if del_text_channels: text_channels = [channel for channel in channels if channel["type"] == 0]
            if del_voc_channels: voc_channels = [channel for channel in channels if channel["type"] == 2]
            if del_categories: categories = [channel for channel in channels if channel["type"] == 4]
            Log(RED, "✓", "Channels successfully scraped")
        except:
            return {"success": False, "message": "Error during scraping channels"}
        
        if del_text_channels:
            for channel in text_channels:
                total += 1
                try:
                    url = f"https://discord.com/api/v9/channels/{channel["id"]}"
                    headers = { "Authorization": token }
                    res = requests.delete(url, headers=headers)
                    if res.status_code == 200:
                        deleted += 1
                        Log(RED, "✓", f"Text Channel {channel["id"]} deleted")
                    else:
                        failed += 1
                        Log(RED, "x", f"Error deleting channel {channel.get("id", "Unknown")}")
                except:
                    failed += 1
                    Log(RED, "x", f"Error deleting channel {channel.get("id", "Unknown")}")
                Title(f"Deleting channels | {deleted} deleted | {failed} failed")
        
        if del_voc_channels:
            for channel in voc_channels:
                total += 1
                try:
                    url = f"https://discord.com/api/v9/channels/{channel["id"]}"
                    headers = { "Authorization": token }
                    res = requests.delete(url, headers=headers)
                    if res.status_code == 200:
                        deleted += 1
                        Log(RED, "✓", f"Text Channel {channel["id"]} deleted")
                    else:
                        failed += 1
                        Log(RED, "x", f"Error deleting channel {channel.get("id", "Unknown")}")
                except:
                    failed += 1
                    Log(RED, "x", f"Error deleting channel {channel.get("id", "Unknown")}")
                Title(f"Deleting channels | {deleted} deleted | {failed} failed")
        
        if del_categories:
            for categorie in categories:
                total += 1
                try:
                    url = f"https://discord.com/api/v9/channels/{categorie["id"]}"
                    headers = { "Authorization": token }
                    res = requests.delete(url, headers=headers)
                    if res.status_code == 200:
                        deleted += 1
                        Log(RED, "✓", f"Text Categorie {categorie["id"]} deleted")
                    else:
                        failed += 1
                        Log(RED, "x", f"Error deleting categorie {categorie.get("id", "Unknown")}")
                except:
                    failed += 1
                    Log(RED, "x", f"Error deleting channel {channel.get("id", "Unknown")}")
                Title(f"Deleting channels | {deleted} deleted | {failed} failed")
        
        return {"success": True, "total": total, "deleted": deleted, "failed": failed}

    def main(self):
        Clear()
        Title("Delete Channels")
        Menu()
        print()
        self.del_text_channels = Ask("You want to delete text channels (y/n)").strip().lower() in ["y", "yes", "o", "oui", "true"]
        self.del_voc_channels = Ask("You want to delete voc channels (y/n)").strip().lower() in ["y", "yes", "o", "oui", "true"]
        self.del_categories = Ask("You want to delete categories (y/n)").strip().lower() in ["y", "yes", "o", "oui", "true"]
        result = self.del_all_channels_func(self.token, self.guild_id, self.del_text_channels, self.del_voc_channels, self.del_categories)
        if not result["success"]:
            SleepLog(RED, "x", result["message"])
            return
        Log(RED, "✓", f"{result["total"]} tried in total | {GREEN}{result["deleted"]}{WHITE} deleted | {RED}{result["failed"]}{WHITE} failed", wp=True)
        input()