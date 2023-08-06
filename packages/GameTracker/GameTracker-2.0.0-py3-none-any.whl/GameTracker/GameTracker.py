import requests
import countries

headers = {"TRN-Api-Key": "2813993b-99c4-4e0c-b511-fa59d121674b"}

class CSGOTracker:
    def __init__(self, playername):
        req = requests.get(f"https://public-api.tracker.gg/v2/csgo/standard/profile/steam/{playername}/", headers=headers)
            
        try:
            self.name = req.json()["data"]["platformInfo"]["platformUserHandle"]
            self.kills = req.json()["data"]["segments"][0]["stats"]["kills"]["value"]
            self.deaths = req.json()["data"]["segments"][0]["stats"]["deaths"]["value"]
            self.kd = req.json()["data"]["segments"][0]["stats"]["kd"]["displayValue"]   
            self.damage = req.json()["data"]["segments"][0]["stats"]["damage"]["displayValue"]
            self.headshots = req.json()["data"]["segments"][0]["stats"]["headshots"]["value"]
            self.shotsFired = req.json()["data"]["segments"][0]["stats"]["shotsFired"]["displayValue"]
            self.shotsAccuracy = req.json()["data"]["segments"][0]["stats"]["shotsAccuracy"]["displayValue"]
            self.bombsPlanted = req.json()["data"]["segments"][0]["stats"]["bombsPlanted"]["displayValue"]
            self.moneyEarned = req.json()["data"]["segments"][0]["stats"]["moneyEarned"]["displayValue"]
            self.wins = req.json()["data"]["segments"][0]["stats"]["wins"]["displayValue"]
            self.losses = req.json()["data"]["segments"][0]["stats"]["losses"]["displayValue"]
            self.matchesPlayed = req.json()["data"]["segments"][0]["stats"]["matchesPlayed"]["displayValue"]
            self.wlr = req.json()["data"]["segments"][0]["stats"]["wlPercentage"]["displayValue"]
            self.hsp = req.json()["data"]["segments"][0]["stats"]["headshotPct"]["displayValue"]
        except:
            print("An unknown error occurred...")

class ApexLegendsTracker:
    def __init__(self, playername, playerplatform):
        req = requests.get(f"https://public-api.tracker.gg/v2/apex/standard/profile/{playerplatform}/{playerplatform}", headers=headers)

        try:
            self.name = req.json()["data"]["platformInfo"]["platformUserHandle"]

            if req.json()["data"]["platformInfo"]["platformUserHandle"] == "psn":
                self.platform = "PlayStation Network"
            elif req.json()["data"]["platformInfo"]["platformUserHandle"] == "xbl":
                self.platform = "Xbox Live"
            else:
                self.platform = "PC"

            self.country = countries.codes[req.json()["data"]["userInfo"]["countryCode"]]

            self.level = req.json()["data"]["segments"][0]["stats"]["level"]["displayValue"]
            self.kills = req.json()["data"]["segments"][0]["stats"]["kills"]["displayValue"]
            self.kpm = req.json()["data"]["segments"][0]["stats"]["kpm"]["displayValue"]
            self.winningkills = req.json()["data"]["segments"][0]["stats"]["winningKills"]["displayValue"]
            self.damage = req.json()["data"]["segments"][0]["stats"]["damage"]["displayValue"]
            self.matchesPlayed = req.json()["data"]["segments"][0]["stats"]["matchsPlayed"]["displayValue"]
            self.revives = req.json()["data"]["segments"][0]["stats"]["revives"]["displayValue"]
            self.sniperkills = req.json()["data"]["segments"][0]["stats"]["sniperKills"]["displayValue"]
        except:
            print("An unknown error occurred.")