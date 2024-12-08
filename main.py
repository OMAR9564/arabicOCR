import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QPushButton, QFileDialog, QMessageBox, QProgressBar
)
from PyQt5.QtCore import Qt
from PIL import Image
import pytesseract


class ImageTextExtractorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Text Extractor")
        self.setGeometry(100, 100, 700, 400)

        self.folder_path = ""
        self.output_folder = ""

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Folder selection layout
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("Selected Folder: No folder selected")
        folder_layout.addWidget(self.folder_label)

        self.browse_button = QPushButton("Select Folder")
        self.browse_button.clicked.connect(self.select_folder)
        folder_layout.addWidget(self.browse_button)
        layout.addLayout(folder_layout)

        # Output folder layout
        output_folder_layout = QHBoxLayout()
        self.output_label = QLabel("Output Folder: Will be created in the selected folder")
        output_folder_layout.addWidget(self.output_label)
        layout.addLayout(output_folder_layout)

        # Extract button
        self.extract_button = QPushButton("Extract Text from Images")
        self.extract_button.clicked.connect(self.extract_texts)
        layout.addWidget(self.extract_button)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

        # Central widget
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder", "")
        if folder:
            self.folder_path = folder
            self.folder_label.setText(f"Selected Folder: {folder}")
            self.output_folder = os.path.join(folder, "Extracted_Text")
            self.output_label.setText(f"Output Folder: {self.output_folder}")

    def extract_texts(self):
        if not self.folder_path:
            QMessageBox.warning(self, "Error", "Please select a folder first!")
            return

        # Ensure output folder exists
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        # Supported formats
        supported_formats = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
        files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(supported_formats)]

        if not files:
            QMessageBox.information(self, "No Images Found", "No supported images found in the selected folder.")
            return

        self.progress_bar.setMaximum(len(files))
        self.progress_bar.setValue(0)

        for idx, file_name in enumerate(files):
            file_path = os.path.join(self.folder_path, file_name)
            try:
                # Perform OCR
                text = pytesseract.image_to_string(Image.open(file_path), lang="ara")

                # Save extracted text to a file
                output_file = os.path.join(self.output_folder, f"{os.path.splitext(file_name)[0]}.txt")
                with open(output_file, "w", encoding="utf-8") as f:
                    f.write(text)

                print(f"Text extracted and saved for: {file_name}")
            except Exception as e:
                print(f"Error processing {file_name}: {e}")

            self.progress_bar.setValue(idx + 1)

        QMessageBox.information(self, "Extraction Complete", f"Text extraction completed. Files saved to:\n{self.output_folder}")


# Run the application
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = ImageTextExtractorApp()
    window.show()
    sys.exit(app.exec_())
