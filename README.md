# GPU-Ebay-Pricing
* Automated eBay listing & price averaging
* Automated plotting of data to existing TomsHardware performance graphs (1080p, 1440p, 4K)
## How to Use
1. Clone the repository
2. Install the required dependencies (`pip install -r requirements.txt`)
3. Run Main.py

After completion, three images will be created in the `output` folder with prices next to GPU names.

Optionally, you can modify Main.py to fit desired behavior. Most notably, writing pricing data to a .csv file using `GPUs.py`'s `WriteData()` function.
## Example Result: 
![USA_1080](https://user-images.githubusercontent.com/117033048/210757463-9fd70c42-28fa-41e0-b10a-75bf32c0d557.png)
