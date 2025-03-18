# PDF Colored Page Counter

A sleek and modern tool for analyzing PDFs and categorizing pages as either black and white or color. This app is perfect for users who need to analyze large documents and identify the types of pages, all while providing a clean, user-friendly interface. Built with PyQt6 for the GUI and PDF2Image for efficient PDF processing.

---

## Features

- **Efficient PDF Analysis**: Automatically processes PDFs and categorizes pages as Black & White or Color.
- **Progress Bar**: Real-time feedback on processing progress with a dynamic, progress bar.
- **Log Viewer**: View detailed logs of the analysis process as the PDF is processed.
- **Simple UI**: Modern and simple interface with clear feedbacks.
- **Robust Performance**: Built to handle large PDFs efficiently and without freezing or crashing.
- **Error Handling**: Handles potential errors gracefully, with clear messages for troubleshooting.


## Requirements

- **Python 3.x**: Ensure Python is installed on your system.
- **Dependencies**:
    - PyQt6
    - pdf2image
    - Pillow
    - numpy
    - PyQt6.QtCore

You can install the dependencies by running:

```bash
pip install -r requirements.txt
```

## How to Run

### Install Dependencies:

1. Clone the repository to your local machine:
    ```bash
    git clone https://github.com/yourusername/PDFColorAnalyzer.git
    ```
2. Navigate to the project folder:
    ```bash
    cd PDFColorAnalyzer
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Run the Application:

After installing the dependencies, simply run the application with:
```bash
python main.py
```

### How It Works
1. Load a PDF: Click on the "Choose PDF" button to select a PDF file.
2. Processing: The app will process each page and classify it as either Black & White or Color. A progress bar will fill up as the PDF is processed.
3. Results: Once the process is complete, the app will display the number of Black & White and Color pages in the PDF.
4. Logs: Detailed logs will be shown during processing, so you can track each page's status.
