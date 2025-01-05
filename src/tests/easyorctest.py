from tqdm import tqdm
import os
import cv2
from ocr.EasyOCRKhawhite import EasyOCRKhawhite
from logger.logger import logger
from pathlib import Path

root_path = Path(".").parent.resolve()
source_path = root_path / "src/data/source_images"
result_path = root_path / "src/data/results"

ocr = EasyOCRKhawhite()
for filename in tqdm(os.listdir(source_path), desc="Processing images..."):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        source_image_path = os.path.join(source_path, filename)
        areas = ocr.findTextAreas()
        for area in areas:
            logger.info(ocr.readText(area))

        painted_image = ocr.paintAreas(areas)
        result_image_path = os.path.join(result_path, filename)
        cv2.imwrite(result_image_path, painted_image)
