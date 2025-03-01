from src.config.utils import *
import requests
import random
import base64
from concurrent.futures import ThreadPoolExecutor
import re

class spammer:
    def __init__(self, token, guild_id):
        self.token = token
        self.guild_id = guild_id
        self.webhook_urls = []
        self.threads_number = 0
        self.number_message_per_webhook = 0
        self.name = None
        self.random_pfp = None
        self.number_webhook_per_channel = 0
        self.message = None
        self.total = 0
        self.sent = 0
        self.failed = 0
    
    def create_webhook(self, channel_id, name=None, random_pfp=False):
        if not name:
            names = ["kersy", "𝑆𝑜𝑠𝑜.", "Jogo", "𝓚𝓲𝓶𝓲", "sixtra", "chillguy", "This' ♛", "Moon 🕷", "Im Just A Girl", "Im Just A Boy", "カネキ "]
            name = random.choice(names)
        url = f"https://discord.com/api/v9/channels/{channel_id}/webhooks"
        headers = { "Authorization": self.token }
        pfp = None
        if random_pfp:
            try:
                png_files = [f for f in os.listdir('assets') if f.endswith('.png')]
                if png_files:
                    pfp = random.choice(png_files)
                    pfp_path = os.path.join("assets", pfp)
                    with open(pfp_path, "rb") as img_file:
                        base64_pfp = base64.b64encode(img_file.read()).decode("utf-8")
                    pfp = f"data:image/png;base64,{base64_pfp}"
            except:
                pfp = None
        payload = {
            "name": name,
            "avatar": pfp
        }
        try:
            res = requests.post(url, headers=headers, json=payload)
            if res.status_code == 200:
                Log(RED, "✓", f"Successfully created webhook {res.json()["id"]} for {res.json()["channel_id"]}")
                return {"success": True, "webhook_url": res.json()["url"]}
            else:
                Log(RED, "x", "Error creating webhook")
                return { "success": False }
        except Exception as e:
            Log(RED, "x", "Error creating webhook")
            return { "success": False }
    
    def create_webhook_for_all_channels(self, number_per_channel: int):
        Log(RED, "!", "Scraping Channels...")
        url = f"https://discord.com/api/v9/guilds/{self.guild_id}/channels"
        headers = { "Authorization": self.token }
        try:
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                Log(RED, "✓", "Channels successfully scraped")
                channels = res.json()
                channels = [channel for channel in channels if channel["type"] == 0]
            else:
                return { "success": False, "message": "Error while scraping channels"}
        except:
            return { "success": False, "message": "Error while scraping channels"}
        
        for channel in channels:
            for i in range(number_per_channel):
                result = self.create_webhook(channel["id"], self.name, self.random_pfp)
                if result["success"]:
                    self.webhook_urls.append(result["webhook_url"])
                time.sleep(random.randint(90, 100)/100)
        return {"success": True, "message": f"{len(self.webhook_urls)} webhooks created" }
    
    def format_message(self, message):
        emoji_pattern = r"\[\[emoji=(\d+)\]\]"
        emojis = ["💀", "😂", "🤣", "⛓️", "♻️", "👑", "🔥", "😭", "🎄", "🚷", "👿", "🦧"]
        string_pattern = r"\[\[string=(\d+)\]\]"
        alphabets = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXY"
        
        def replace_match_emoji(match):
            num = int(match.group(1))
            num = min(max(num, 1), 100)
            return "".join(random.choices(emojis, k=num))
        
        def replace_match_string(match):
            num = int(match.group(1))
            num = min(max(num, 1), 100)
            return "".join(random.choices(alphabets, k=num))
        
        message = re.sub(emoji_pattern, replace_match_emoji, message)
        message = re.sub(string_pattern, replace_match_string, message)
        return message

    def spam_message_with_webhook(self, webhook_url):
        for i in range(int(self.number_message_per_webhook)):
            self.total += 1
            message = self.format_message(self.message)
            payload = { "content": message }
            try:
                res = requests.post(webhook_url, json=payload)
                if res.status_code == 204:
                    self.sent += 1
                    Log(RED, "✓", f"Sent with {webhook_url.split('/')[-1][:50]}*****")
                else:
                    self.failed += 1
                    Log(RED, "x", f"Failed with {webhook_url.split('/')[-1][:50]}*****")
            except:
                self.failed += 1
                Log(RED, "x", f"Failed with {webhook_url.split('/')[-1][:50]}*****")
            time.sleep(random.randint(90, 100)/100)
    
    def main(self):
        Clear()
        Title("Spammer")
        Menu()
        print()
        self.name = Ask("Webhook name (leave blank for random)").strip()
        self.random_pfp = Ask("Include random profile picture (y/n)").strip().lower() in ["y", "yes", "o", "oui", "true"]
        self.number_webhook_per_channel = Ask("Number of webhook per channel (max 15)").strip()
        if not self.number_webhook_per_channel.isdigit() or int(self.number_webhook_per_channel) <= 0 or int(self.number_webhook_per_channel) > 15:
            SleepLog(RED, "x", "Invalid number")
            return
        self.message = Ask("Message to spam (u can use var: [[emoji=10] or [[string=15]]])").strip()
        if not self.message:
            SleepLog(RED, "x", "Message cannot be empty")
            return
        self.number_message_per_webhook = Ask("Number of message per webhook").strip()
        if not self.number_message_per_webhook.isdigit() or int(self.number_message_per_webhook) <= 0:
            SleepLog(RED, "x", "Invalid number")
            return
        self.threads_number = Ask("Number of threads (default 10)").strip()
        if not self.threads_number.isdigit() or int(self.threads_number) <= 0:
            self.threads_number = 10
        
        Clear()
        Title("Creating webhooks")
        Menu()
        print()
        result = self.create_webhook_for_all_channels(int(self.number_webhook_per_channel))
        if not result["success"]:
            Log(RED, "x", result["message"], wp=True)
            input()
            return
        Log(RED, "✓", result["message"])

        Title("Spamming")
        with ThreadPoolExecutor(max_workers=int(self.threads_number)) as executor:
                executor.map(self.spam_message_with_webhook, self.webhook_urls)
        Log(RED, "✓", f"{self.total} tried in total | {GREEN}{self.sent}{WHITE} sent | {RED}{self.failed}{WHITE} failed", wp=True)
        input()