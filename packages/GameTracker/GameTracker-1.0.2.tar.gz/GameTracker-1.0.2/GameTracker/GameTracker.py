import requests

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