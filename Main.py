import datetime
from PIL import Image, ImageDraw, ImageFont, ImageOps
from GPUs import LoadGPUs, WriteData_CSV, GPU
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
    
def _testCoordinates(gpus: list, gpuName: str):
    fhdImage = Image.open('./bin/1080.png')
    qhdImage = Image.open('./bin/1440.png')
    fourKImage = Image.open('./bin/4K.png')

    fhdImage_Draw = ImageDraw.Draw(fhdImage)
    qhdImage_Draw = ImageDraw.Draw(qhdImage)
    fourKImage_Draw = ImageDraw.Draw(fourKImage)

    for gpu in gpus:
        if gpu.ModelName == gpuName:
            break

    if gpu.Coordinates[0] != "" and gpu.Coordinates[0] is not None:
        fhdImage_Draw.text(
            (int(gpu.Coordinates[0].split(",")[0]), int(gpu.Coordinates[0].split(",")[1])),
            f"$899", fill=(255, 0, 0), font=priceFont
        )
        
    if gpu.Coordinates[1] != "" and gpu.Coordinates[1] is not None:
        qhdImage_Draw.text(
            (int(gpu.Coordinates[1].split(",")[0]), int(gpu.Coordinates[1].split(",")[1])),
            f"$899", fill=(255, 0, 0), font=priceFont
        )
        
    if gpu.Coordinates[2] != "" and gpu.Coordinates[2] is not None:
        fourKImage_Draw.text(
            (int(gpu.Coordinates[2].split(",")[0]), int(gpu.Coordinates[2].split(",")[1])),
            f"$899", fill=(255, 0, 0), font=priceFont
        )

    now = datetime.datetime.now()
    currentDateStr = now.strftime(f"%B %d, %Y")

    fourKImage_Draw.text((870, 250), f"Test Pricing", fill=(255, 0, 0), font=titleFont)
    fourKImage_Draw.text((1015, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    fourKImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    fhdImage_Draw.text((870, 250), f"Test Pricing", fill=(255, 0, 0), font=titleFont)
    fhdImage_Draw.text((1015, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    fhdImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    qhdImage_Draw.text((872, 250), f"Test Pricing", fill=(255, 0, 0), font=titleFont)
    qhdImage_Draw.text((1017, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    qhdImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    fhdImage.save(f'./Test_1080.png')
    qhdImage.save(f'./Test_1440.png')
    fourKImage.save(f'./Test_4K.png')


def GenerateGraphs(region: str, currency: str, darkMode: bool = False):
    fhdImage = Image.open('./bin/1080.png')
    qhdImage = Image.open('./bin/1440.png')
    fourKImage = Image.open('./bin/4K.png')

    fhdImage_Draw = ImageDraw.Draw(fhdImage)
    qhdImage_Draw = ImageDraw.Draw(qhdImage)
    fourKImage_Draw = ImageDraw.Draw(fourKImage)

    progressBar = tqdm.tqdm(total = len(gpus), unit="GPU")
    for gpu in gpus:
        progressBar.set_description(desc=f"{region: >3} Prices | {gpu.ModelName: <16}")
        gpu.GrabListings(region=region)
        progressBar.update(1)
        
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

    fourKImage_Draw.text((870, 250), f"{region} Pricing", fill=(255, 0, 0), font=titleFont)
    fourKImage_Draw.text((1015, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    fourKImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    fhdImage_Draw.text((870, 250), f"{region} Pricing", fill=(255, 0, 0), font=titleFont)
    fhdImage_Draw.text((1015, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    fhdImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)

    qhdImage_Draw.text((872, 250), f"{region} Pricing", fill=(255, 0, 0), font=titleFont)
    qhdImage_Draw.text((1017, 305), currentDateStr, fill=(255, 0, 0), font=priceFont)
    qhdImage_Draw.text((110, 970), "No affiliation with TomsHardware (just using their performance graphs)", fill=(255, 0, 0), font=priceFont)


    if darkMode:
        fhdImage = _invertImage(fhdImage)
        qhdImage = _invertImage(qhdImage)
        fourKImage = _invertImage(fourKImage)

    fhdImage.save(f'./{region}_1080.png')
    qhdImage.save(f'./{region}_1440.png')
    fourKImage.save(f'./{region}_4K.png')

    progressBar.set_description(desc=f"{region: >3} Prices | Complete!       ")
    progressBar.close()

if __name__ == "__main__":
    GenerateGraphs("USA Ebay", "$", darkMode=True) # Region name from ./bin/Regions.json entries 