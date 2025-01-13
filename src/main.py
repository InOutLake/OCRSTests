from tests import easyorctest, tesseracttest
import multiprocessing

if __name__ == "__main__":
    # multiprocessing.freeze_support()
    # p = multiprocessing.Process(target=easyorctest.easyocr_draw_areas()())
    # p.start()
    tesseracttest.tesseract_draw_areas()
