def load_styles():
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
