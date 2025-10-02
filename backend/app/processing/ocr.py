from manga_ocr import MangaOcr

class OcrProcessor():
    def __init__(self):
        self.mocr = MangaOcr()

    def extract_text(self, text):
        return self.mocr(text)

    