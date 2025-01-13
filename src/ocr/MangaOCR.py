from manga_ocr import MangaOcr
from PIL import Image


class MangaOCR:
    def __init__(self):
        self.image = None
        self.mocr = MangaOcr()

    def selectImage(self, image_path: str) -> None:
        self.image = Image.open(image_path)
