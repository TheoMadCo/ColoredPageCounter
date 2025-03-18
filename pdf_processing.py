import numpy as np
from PyQt6.QtCore import QThread, pyqtSignal
from pdf2image import convert_from_path
from PIL import Image

class PDFProcessingThread(QThread):
    progress_signal = pyqtSignal(int)
    log_signal = pyqtSignal(str)
    result_signal = pyqtSignal(int, int)
    error_signal = pyqtSignal(str)

    def __init__(self, pdf_path):
        super().__init__()
        self.pdf_path = pdf_path

    def is_grayscale(self, image: Image.Image) -> bool:
        """ Check if an image is grayscale """
        if image.mode != "RGB":
            image = image.convert("RGB")
        im_array = np.array(image)
        return np.all(im_array[:, :, 0] == im_array[:, :, 1]) and np.all(im_array[:, :, 1] == im_array[:, :, 2])

    def run(self):
        """ Process the PDF file in a separate thread """
        try:
            pages = convert_from_path(self.pdf_path, dpi=50)
            total_pages = len(pages)
            bw_count, color_count = 0, 0

            self.log_signal.emit(f"📄 Total pages found: {total_pages}\n🔄 Processing started...\n")
            self.progress_signal.emit(0)  # Start progress bar at 0%

            for i, page in enumerate(convert_from_path(self.pdf_path, dpi=150), start=1):
                if self.is_grayscale(page):
                    bw_count += 1
                    self.log_signal.emit(f"✅ Page {i}: Black & White")
                else:
                    color_count += 1
                    self.log_signal.emit(f"🎨 Page {i}: Color")

                progress = int((i / total_pages) * 100)
                self.progress_signal.emit(progress)  # Fill up progress bar correctly

            self.result_signal.emit(bw_count, color_count)
        except Exception as e:
            self.error_signal.emit(str(e))
