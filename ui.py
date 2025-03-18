from PyQt6.QtWidgets import QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout, QProgressBar, QTextEdit, QFrame
from PyQt6.QtCore import Qt
from pdf_processing import PDFProcessingThread  # Importa il modulo di elaborazione PDF
from styles import load_styles  # Importa gli stili

class PDFAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        """ Setup the UI elements """
        self.setWindowTitle("PDF Color Analyzer")
        self.setGeometry(100, 100, 500, 420)
        self.setStyleSheet(load_styles())  # Applica lo stile

        self.label = QLabel("📄 Select a PDF file to analyze", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Choose PDF", self)
        self.button.clicked.connect(self.load_pdf)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)

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
        self.progress_bar.setValue(100)

    def show_error(self, message):
        """ Show an error message if processing fails """
        self.result_label.setText(f"<b style='color:red;'>⚠️ Error:</b> {message}")
