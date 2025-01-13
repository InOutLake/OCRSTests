import pytesseract
from pytesseract import Output
import cv2
import copy


class TesseractOCR:
    def __init__(self):
        self.image = None

    def selectImage(self, image_path: str) -> None:
        self.image = cv2.imread(image_path)
        self.image_name = image_path

    def findTextAreas(self) -> dict:
        areas = pytesseract.image_to_boxes(
            self.image, lang="jpn_vert+jpn", output_type=Output.DICT, config="--psm 1"
        )
        return areas

    def drawAreas(self, areas: dict) -> cv2.Mat:
        painted_image = copy.deepcopy(self.image)
        for i in range(len(list(areas.values())[0])):
            cv2.rectangle(
                painted_image,
                (areas["left"][i], areas["top"][i]),
                (areas["right"][i], areas["bottom"][i]),
                (255, 0, 0),
                3,
            )
            cv2.putText(
                painted_image,
                str(i),
                (areas["left"][i], areas["top"][i] - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.9,
                (0, 0, 255),
                2,
            )
        return painted_image
