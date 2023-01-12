import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
from GPUs import LoadGPUs
import tqdm

gpus = LoadGPUs()

priceFont = ImageFont.truetype("segoeui.ttf", 18)
titleFont = ImageFont.truetype("segoeuib.ttf", 48)

def _invertImage(image):
    if image.mode != "RGBA":
        return ImageOps.invert(image)
    r,g,b,a = image.split()
    rgbImage = Image.merge("RGB", (r,g,b))
        
    invertedImage = ImageOps.invert(rgbImage)
    r,g,b = invertedImage.split()
    finalImage = Image.merge("RGBA", (r,g,b,a))
    return finalImage
    

def GenerateGraphs(region: str, currency: str, darkMode: bool = False):
    fhdImage = Image.open('./bin/1080.png')
    qhdImage = Image.open('./bin/1440.png')
    fourKImage = Image.open('./bin/4K.png')

    fhdImage_Draw = ImageDraw.Draw(fhdImage)
    qhdImage_Draw = ImageDraw.Draw(qhdImage)
    fourKImage_Draw = ImageDraw.Draw(fourKImage)

    for gpu in tqdm.tqdm(gpus, desc=f"{region} eBay Prices", position=0, leave=True):
        gpu.GrabListings(region=region)
        region = region.upper()
        
        if gpu.Coordinates[0] == "" or gpu.Coordinates[0] is None:
            continue
        fhdImage_Draw.text(
            (int(gpu.Coordinates[0].split(",")[0]), int(gpu.Coordinates[0].split(",")[1])),
            f"{currency}{round(gpu.GetAveragePrice())}", fill=(255, 0, 0), font=priceFont
        )
        
        if gpu.Coordinates[1] == "" or gpu.Coordinates[1] is None:
            continue
        qhdImage_Draw.text(
            (int(gpu.Coordinates[1].split(",")[0]), int(gpu.Coordinates[1].split(",")[1])),
            f"{currency}{round(gpu.GetAveragePrice())}", fill=(255, 0, 0), font=priceFont
        )
        
        if gpu.Coordinates[2] == "" or gpu.Coordinates[2] is None:
            continue
        fourKImage_Draw.text(
            (int(gpu.Coordinates[2].split(",")[0]), int(gpu.Coordinates[2].split(",")[1])),
            f"{currency}{round(gpu.GetAveragePrice())}", fill=(255, 0, 0), font=priceFont
        )
    now = datetime.datetime.now()
    currentDateStr = now.strftime(f"%B %d, %Y")

    fourKImage_Draw.text((870, 250), f"{region} Ebay Pricing", fill=(255, 0, 0), font=titleFont)
    fourKImage_Draw.text((1015, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    fourKImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    fhdImage_Draw.text((870, 250), f"{region} Ebay Pricing", fill=(255, 0, 0), font=titleFont)
    fhdImage_Draw.text((1015, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    fhdImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    qhdImage_Draw.text((872, 250), f"{region} Ebay Pricing", fill=(255, 0, 0), font=titleFont)
    qhdImage_Draw.text((1017, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    qhdImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)


    if darkMode:
        fhdImage = _invertImage(fhdImage)
        qhdImage = _invertImage(qhdImage)
        fourKImage = _invertImage(fourKImage)

    fhdImage.save(f'./{region}_1080.png')
    qhdImage.save(f'./{region}_1440.png')
    fourKImage.save(f'./{region}_4K.png')


if __name__ == "__main__":
    GenerateGraphs("USA", "$", darkMode=True) # Region name from ./bin/Regions.json entries
    GenerateGraphs("UK", "£") # Currency symbol is used only for the graphs, this can be whatever you want.
    GenerateGraphs("CA", "C$")
    GenerateGraphs("AU", "A$")
    GenerateGraphs("DE", "€")