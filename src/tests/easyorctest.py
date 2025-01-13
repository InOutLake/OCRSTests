from tqdm import tqdm
import cv2
import importlib
from ocr.EasyOCRKhawhite import EasyOCRKhawhite
from pathlib import Path
import json
from itertools import islice

importlib.import_module("ocr")

source_path = Path(".") / "Manga109s" / "images"
result_path = Path(".") / "src" / "data" / "results" / "easyocr"
result_images_path = result_path / "images"
result_images_path.mkdir(parents=True, exist_ok=True)
result_json_file = result_path / "results.json"


def easyocr_draw_areas():
    ocr = EasyOCRKhawhite()
    for source_manga_path in islice(source_path.iterdir(), 10):
        result_manga_path = result_images_path / source_manga_path.name
        result_manga_path.mkdir(parents=True, exist_ok=True)
        for source_image_path in tqdm(
            islice(source_manga_path.iterdir(), 5),
            desc=f"Processing {source_manga_path.name} images...",
        ):
            ocr.selectImage(source_image_path)
            areas = ocr.findTextAreas()
            painted_image = ocr.drawAreas(areas)
            result_image_path = result_manga_path / source_image_path.name
            cv2.imwrite(result_image_path, painted_image)


def save_all_txt():
    ocr = EasyOCRKhawhite()
    with result_json_file.open("w") as f:
        for source_image_path in tqdm(
            source_path.iterdir(), desc="Processing images..."
        ):
            ocr.selectImage(source_image_path)
            results = ocr.findAndReadAll()
            f.write(json.dump(results))


if __name__ == "__main__":
    easyocr_draw_areas()()
