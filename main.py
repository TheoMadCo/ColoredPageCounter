import sys
import numpy as np
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, 
    QProgressBar, QTextEdit, QFrame
)
from PyQt6.QtCore import QThread, pyqtSignal, Qt
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

class PDFAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """ Setup the UI elements """
        self.setWindowTitle("PDF Color Analyzer")
        self.setGeometry(100, 100, 500, 420)
        self.setStyleSheet(self.load_styles())

        self.label = QLabel("📄 Select a PDF file to analyze", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Choose PDF", self)
        self.button.clicked.connect(self.load_pdf)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)  # Start empty

        self.log_box = QTextEdit(self)
        self.log_box.setReadOnly(True)
        self.log_box.setFrameShape(QFrame.Shape.StyledPanel)

        self.result_label = QLabel("", self)
        self.result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.log_box)
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def load_pdf(self):
        """ Open a file dialog to select a PDF file """
        file_path, _ = QFileDialog.getOpenFileName(self, "Open PDF File", "", "PDF Files (*.pdf);;All Files (*)")

        if file_path:
            self.label.setText(f"🔍 Processing: {file_path.split('/')[-1]}")
            self.result_label.setText("")
            self.progress_bar.setValue(0)
            self.log_box.clear()

            # Run in a separate thread
            self.thread = PDFProcessingThread(file_path)
            self.thread.progress_signal.connect(self.progress_bar.setValue)
            self.thread.log_signal.connect(self.update_log)
            self.thread.result_signal.connect(self.display_results)
            self.thread.error_signal.connect(self.show_error)
            self.thread.start()

    def update_log(self, message):
        """ Append messages to the log box """
        self.log_box.append(message)

    def display_results(self, bw_count, color_count):
        """ Display final results """
        self.result_label.setText(
            f"<b>🖤 Black & White Pages:</b> {bw_count} ✅<br>"
            f"<b>🎨 Color Pages:</b> {color_count} 🎨"
        )
        self.progress_bar.setValue(100)  # Ensure full at the end

    def show_error(self, message):
        """ Show an error message if processing fails """
        self.result_label.setText(f"<b style='color:red;'>⚠️ Error:</b> {message}")

    def load_styles(self):
        """ Load the CSS-like style for accessible UI """
        return """
            QWidget {
                background-color: #2C2F33; /* Dark Gray */
                font-family: Arial, sans-serif;
                font-size: 14px;
                color: white;
            }
            QLabel {
                font-size: 16px;
                font-weight: bold;
                padding: 10px;
                color: #FFFFFF;
            }
            QPushButton {
                background-color: #00A86B; /* Green */
                color: white;
                padding: 8px;
                border-radius: 5px;
                font-size: 14px;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #008B5E;
            }
            QProgressBar {
                border: 2px solid gray;
                border-radius: 5px;
                text-align: center;
                font-weight: bold;
                background-color: #444;
                color: white;
            }
            QProgressBar::chunk {
                background-color: #00A86B;
            }
            QTextEdit {
                background-color: #FFFFFF;
                border: 1px solid #ccc;
                padding: 5px;
                border-radius: 5px;
                font-size: 12px;
                color: black;
            }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFAnalyzer()
    window.show()
    sys.exit(app.exec())
