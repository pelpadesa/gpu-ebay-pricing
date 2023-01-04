import json
from bs4 import BeautifulSoup
import requests
import time

class Listing:
    def __init__(self, Title, Subtitle, Price) -> None:
        self.Title = Title
        self.Subtitle = Subtitle
        self.Price = self.SetPrice(Price)
    def SetPrice(self, price: str):
        # $1,900.00
        price = price.split(".")[0] if "." in price else price
        price = price.replace("$", "").replace(",", "")
        return int(price)
class GPU:
    def __init__(self, ModelName: str, Coordinates: list) -> None:
        self.ModelName = ModelName
        self.Listings = []
        self.Coordinates = Coordinates
    def GetAveragePrice(self):
        price = 0
        for listing in self.Listings:
            price += listing.Price
        price = price / len(self.Listings)
        return price
    def GrabListings(self):
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        url = f"https://www.ebay.com/sch/i.html?_from=R40&_nkw=\"{self.ModelName}\"&_sacat=0&rt=nc&LH_Sold=1&LH_Complete=1"
        soup = BeautifulSoup(
            requests.get(url, headers=headers).text,
            features='lxml'
        )
        listings = soup.select("#srp-river-results > ul > li")
        for item in listings:
            listingTitle = item.select_one("div > div.s-item__info.clearfix > a > div > span")
            listingPrice = item.select_one("div > div.s-item__info.clearfix > div.s-item__details.clearfix > div:nth-child(1) > span > span")
            if listingTitle is None:
                continue
            if listingPrice is None:
                continue

            gpuListing = Listing(
                Title = listingTitle.text,
                Subtitle = item.select_one("div > div.s-item__info.clearfix > div.s-item__subtitle"),
                Price = listingPrice.text
            )
            _title = listingTitle.text.lower()
            if "nvlink" in _title or "sli bridge" in _title or "parts" in _title or "repair" in _title or "block" in _title or "description" in _title or "faulty" in _title or " for " in _title or "only" in _title or "as is" in _title or "not working" in _title or "box" in _title:
                continue
            self.Listings.append(gpuListing)
        time.sleep(0.2)

def LoadGPUs():
    gpus = []
    jsonData = json.loads(open("GPUs.json", "r").read())
    for gpu in jsonData:
        gpuObj = GPU(
            ModelName = gpu,
            Coordinates = [
                jsonData[gpu].get("1080p"),
                jsonData[gpu].get("1440p"),
                jsonData[gpu].get("4K")
            ]
        )
        gpus.append(gpuObj)
    return gpus

def WriteData_CSV(gpus: list):
    with open("pricing_data.csv", "w+") as dataFile:
        for gpu in gpus:
            dataFile.write(f"{gpu.ModelName},{gpu.GetAveragePrice()}\n")