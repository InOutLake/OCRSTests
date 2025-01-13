from manga_ocr import MangaOcr
import easyocr
import numpy as np
import cv2
import copy
from PIL import Image


class EasyOCRKhawhite:
    def __init__(self):
        self.reader = easyocr.Reader(lang_list=["ja"], gpu=True)
        self.mocr = MangaOcr()
        self.image_name: str | None = None
        self.image: cv2.Mat | None = None
        self.readtext_params = {
            "batch_size": 32,
            "workers": 0,
            "y_ths": 0.13,
            "x_ths": 0.18,
            "paragraph": True,
            "min_size": 10,
            "text_threshold": 0.4,
            "slope_ths": 0.01,
            "add_margin": 0.001,
            "height_ths": 0.3,
            "width_ths": 0.2,
        }

    def selectImage(self, image_path: str) -> None:
        self.image = cv2.imread(image_path)

    def findTextAreas(self) -> np.ndarray:
        # Using readtext() instead of detect() because of "paragraph" param,
        # which makes merging boxes way less comlicated
        areas = self.reader.readtext(self.image, detail=1, **self.readtext_params)
        return np.int_([item[0] for item in areas])

    def readText(self, area: np.ndarray) -> str:
        text_area_image = self.image[area[0][1] : area[2][1], area[0][0] : area[2][0]]
        text_area_image = cv2.cvtColor(text_area_image, cv2.COLOR_BGR2GRAY)

        text_area_image = Image.fromarray(text_area_image)
        text = self.mocr(text_area_image)
        return text

    def findAndReadAll(self) -> dict:
        areas = self.findTextAreas()
        result = {}
        for area in areas:
            text = self.readText(area)
            result.setdefault(text, area)
        return result

    def drawAreas(self, areas: np.ndarray) -> cv2.Mat:
        painted_image = copy.deepcopy(self.image)
        for i, area in enumerate(areas):
            cv2.rectangle(
                painted_image,
                tuple([int(start_cords) for start_cords in area[0]]),
                tuple([int(end_cords) for end_cords in area[2]]),
                (255, 0, 0),
                3,
            )
            cv2.putText(
                painted_image,
                str(i),
                (area[0][0], area[0][1] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2,
            )
        return painted_image
