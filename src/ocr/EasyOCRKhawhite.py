from manga_ocr import MangaOcr
import easyocr
import numpy as np
import cv2
import PIL
import copy


class EasyOCRKhawhite:
    def __init__(self, reader_params: dict):
        reader_params.setdefault("lang_list", ["ja", "en"])
        reader_params.setdefault("gpu", True)
        self.reader = easyocr.Reader(**reader_params)
        self.mocr = MangaOcr()
        self.image_name: str | None = None
        self.image: cv2.Mat | None = None

    def selectImage(self, image_path: str) -> None:
        self.image = PIL.Image.open(image_path)
        self.image_name = image_path

    def findTextAreas(self) -> cv2.Mat:
        # Using readtext() instead of detect() because of "paragraph" param,
        # which makes merging boxes way less comlicated
        areas = self.reader.readtext(
            self.image, detail=0, y_ths=1, x_ths=1, paragraph=True
        )
        return areas

    def readText(self, area: np.ndarray) -> str:
        text_area_image = self.image[area[0][0] : area[2][0], area[0][1] : area[2][1]]
        text = self.mocr(text_area_image)
        return text

    def findAndReadAll(self) -> dict:
        areas = self.findTextAreas()
        result = {}
        for area in areas:
            text = self.readText(area)
            result.setdefault(text, area)
        return result

    def paintAreas(self, areas: np.ndarray) -> cv2.Mat:
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
