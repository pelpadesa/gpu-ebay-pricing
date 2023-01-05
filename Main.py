import datetime
from PIL import Image, ImageDraw, ImageFont
from GPUs import LoadGPUs

gpus = LoadGPUs()

fhdImage = Image.open('./bin/1080.png')
fhdImage_Draw = ImageDraw.Draw(fhdImage)

qhdImage = Image.open('./bin/1440.png')
qhdImage_Draw = ImageDraw.Draw(qhdImage)

fourKImage = Image.open('./bin/4K.png')
fourKImage_Draw = ImageDraw.Draw(fourKImage)

priceFont = ImageFont.truetype("segoeui.ttf", 16)
titleFont = ImageFont.truetype("segoeuib.ttf", 48)

REGION = "USA"
CURRENCY = "$"

for gpu in gpus:
    gpu.GrabListings(region=REGION)
    REGION = REGION.upper()
        
    if gpu.Coordinates[0] == "" or gpu.Coordinates[0] is None:
        print(f"{gpu.ModelName} | Average Price: {CURRENCY}{gpu.GetAveragePrice()}")
        continue
    fhdImage_Draw.text((int(gpu.Coordinates[0].split(",")[0]), int(gpu.Coordinates[0].split(",")[1])), f"{CURRENCY}{round(gpu.GetAveragePrice())}", fill=(255, 0, 0), font=priceFont)
        
    if gpu.Coordinates[1] == "" or gpu.Coordinates[1] is None:
        print(f"{gpu.ModelName} | Average Price: {CURRENCY}{gpu.GetAveragePrice()}")
        continue
    qhdImage_Draw.text((int(gpu.Coordinates[1].split(",")[0]), int(gpu.Coordinates[1].split(",")[1])), f"{CURRENCY}{round(gpu.GetAveragePrice())}", fill=(255, 0, 0), font=priceFont)
        
    if gpu.Coordinates[2] == "" or gpu.Coordinates[2] is None:
        print(f"{gpu.ModelName} | Average Price: {CURRENCY}{gpu.GetAveragePrice()}")
        continue
    fourKImage_Draw.text((int(gpu.Coordinates[2].split(",")[0]), int(gpu.Coordinates[2].split(",")[1])), f"{CURRENCY}{round(gpu.GetAveragePrice())}", fill=(255, 0, 0), font=priceFont)
    print(f"{gpu.ModelName} | Average Price: {CURRENCY}{gpu.GetAveragePrice()}")
    
now = datetime.datetime.now()
currentDateStr = now.strftime(f"%B %d, %Y")

fourKImage_Draw.text((670, 250), f"{REGION} Ebay Pricing", fill=(255, 0, 0), font=titleFont)
fourKImage_Draw.text((915, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)

fhdImage_Draw.text((670, 250), f"{REGION} Ebay Pricing", fill=(255, 0, 0), font=titleFont)
fhdImage_Draw.text((915, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    
qhdImage_Draw.text((742, 250), f"{REGION} Ebay Pricing", fill=(255, 0, 0), font=titleFont)
qhdImage_Draw.text((987, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    
fhdImage.save('./output_1080.png')
qhdImage.save('./output_1440.png')
fourKImage.save('./output_4K.png')
