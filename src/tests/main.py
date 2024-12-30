from tqdm import tqdm
import easyocr
import os

root_path = os.getcwd()
source_path = os.path.join(root_path, "src/data/source_images")

for filename in tqdm(os.listdir(source_path), desc="Processing images..."):
    reader = easyocr.Reader(["ja", "en"])
    if filename.endswith(".jpg") or filename.endswith(".png"):
        image_path = os.path.join(source_path, filename)
        result = reader.readtext(image_path, detail=1)
        print(list([item[1] for item in result]))
