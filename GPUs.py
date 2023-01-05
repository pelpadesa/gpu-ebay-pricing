import json
from bs4 import BeautifulSoup
import requests
import time

class Listing:
    def __init__(self, Title, Price) -> None:
        self.Title = Title
        self.Price = self.SetPrice(Price)
    def SetPrice(self, price: str):
        # $1,900.00
        price = price.split(".")[0] if "." in price else price

        price_ = ""
        for char in price:
            if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
                price_ += char
        return int(price_)
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
    def GetLowestPrice(self):
        currentPrice = 9999999
        for listing in self.Listings:
            if listing.Price < currentPrice:
                # Only get the lowest priced listing if it's above 70% the average price, else it could be bad data or not representative.
                currentPrice = listing.Price if (self.GetAveragePrice() / 1.3) < listing.Price else currentPrice
        return currentPrice
    def GrabListings(self, region: str = "USA"):
        with open("./bin/Regions.json") as regionFile:
            region = json.loads(regionFile.read()).get(region.upper())
        listings_Selector = region.get("listings")
        listing_Title = region.get("listingTitle")
        listing_Price = region.get("listingPrice")
        Currency = region.get("Currency")
        requestURL = region.get("URL_Part1") + self.ModelName + region.get("URL_Part2")
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
        }
        soup = BeautifulSoup(
            requests.get(requestURL, headers=headers).text,
            features='lxml'
        )
        listings = soup.select(listings_Selector)
        for item in listings:
            listingTitle = item.select_one(listing_Title)
            listingPrice = item.select_one(listing_Price)
            if listingTitle is None:
                continue
            if listingPrice is None:
                continue
            
            _title = listingTitle.text.lower()
            for phrase in ["nvlink", "sli bridge", "parts", "repair", "block", "description", "faulty", " for ", "only", "as is", "not working", "box", "*for "]:
                if phrase in _title:
                    break
            if phrase in _title: # This is either really neat or really overcomplicated
                continue

            gpuListing = Listing(
                Title = listingTitle.text,
                Price = listingPrice.text,
                listingCurrency = Currency
            )
            
            self.Listings.append(gpuListing)
        time.sleep(0.2)

def LoadGPUs():
    gpus = []
    jsonData = json.loads(open("./bin/GPUs.json", "r").read())
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
    with open("./pricing_data.csv", "w+") as dataFile:
        for gpu in gpus:
            dataFile.write(f"{gpu.ModelName},{gpu.GetAveragePrice()}\n")