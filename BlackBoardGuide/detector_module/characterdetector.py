import pyocr


class CharacterDetector():
    def __init__(self):
        self.ocr_tool = pyocr.tesseract()

    def detect_charactor(self, target_image, langage='jpn'):
        detect_text = self.ocr_tool.image_to_string(target_image, langage)
        return detect_text
