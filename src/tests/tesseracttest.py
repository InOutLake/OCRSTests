from ocr.TesseractOCR import TesseractOCR
from pathlib import Path
from logger.logger import logger
from tqdm import tqdm
import cv2
from itertools import islice

source_path = Path(".") / "Manga109s" / "images"
result_path = Path(".") / "src" / "data" / "results" / "tesseract"
result_images_path = result_path / "images"
result_images_path.mkdir(parents=True, exist_ok=True)
result_json_file = result_path / "results.json"


def tesseract_draw_areas():
    ocr = TesseractOCR()
    for manga in islice(source_path.iterdir(), 10):
        result_manga_folder = result_images_path / manga.name
        result_manga_folder.mkdir(parents=True, exist_ok=True)
        for image in tqdm(
            islice(manga.iterdir(), 5), desc=f"Processing {manga} images..."
        ):
            ocr.selectImage(image)
            areas = ocr.findTextAreas()
            if areas:
                painted_image = ocr.drawAreas(areas)
                result_image_path = result_manga_folder / image.name
                cv2.imwrite(result_image_path, painted_image)
