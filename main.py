import sys
from PyQt6.QtWidgets import QApplication
from ui import PDFAnalyzer  # Importa l'interfaccia utente
from pdf_processing import PDFProcessingThread  # Importa la logica di elaborazione

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PDFAnalyzer()  # Crea l'istanza della finestra principale
    window.show()  # Mostra la finestra
    sys.exit(app.exec())  # Esegui l'app
