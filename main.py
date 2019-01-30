import requests, json, sys, time
import os.path as fs
from unidecode import unidecode
from html import unescape
# Variables
SOURCE_URL = "https://github.com/MineRobber9000/prequelupdatebot"
PREQUEL_API = "http://ny1.hashbang.sh:1046" # run your own and put the url here!
# webhook testing server
WEBHOOK_URL = "https://discordapp.com/api/webhooks/484022315928256513/ozspOJFywMB_nehT8onOk-GCKevfxbCWB6XfwX76O9zQzuZYrI0mEsNq3BmW1MqH_7zf"
if fs.exists("webhook.txt"):
	with open("webhook.txt") as f:
		WEBHOOK_URL = f.read().strip()
with open("webhook.json") as f: WEBHOOK_DEFAULT = json.load(f)
global lasturl
if fs.exists("lastid"):
	with open("lastid") as f:
		lasturl = f.read()
else:
	lasturl = "nope screw you"

resp = requests.get(PREQUEL_API+"/api/latest")
resp.raise_for_status()
r = resp.json()
if lasturl==r["link"]:
	sys.exit(0)
webhook = {}
webhook.update(WEBHOOK_DEFAULT)
embed = webhook["embeds"][0]
embed["title"] = "New Update: "+r["title"]
embed["url"] = r["link"]
embed["description"] = "```"+unidecode(unescape(r["summary"]))+"```\nUpdated {}\nFound on {}\nUpdate bot source: {}".format(r["published"],time.strftime("%Y-%m-%d"),SOURCE_URL)
webhook["embeds"][0] = embed
headers = {"Content-Type":"application/json"}
data = json.dumps(webhook)
p = requests.post(WEBHOOK_URL,data=data,headers=headers)
with open("lastid","w") as f:
	f.write(r["link"])
