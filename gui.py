from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QLabel, QFileDialog, QVBoxLayout,
    QLineEdit, QHBoxLayout, QListWidget, QMessageBox, QSpinBox
)
from PyQt5.QtCore import Qt
import os
from exif_reader import get_taken_date
from renamer import rename_photos
from utils import is_image_file

class PhotoRenamerApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Photo Renamer")
        self.setGeometry(300, 200, 600, 400)

        self.folder_path = ""
        self.file_list = []

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Folder selector
        folder_layout = QHBoxLayout()
        self.folder_label = QLabel("No folder selected")
        browse_btn = QPushButton("Browse Folder")
        browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_label)
        folder_layout.addWidget(browse_btn)

        # Filename format input
        self.format_input = QLineEdit("IMG_{num:06d}.{ext}")
        self.start_num_input = QSpinBox()
        self.start_num_input.setValue(1)
        self.start_num_input.setMinimum(1)

        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("Format:"))
        format_layout.addWidget(self.format_input)
        format_layout.addWidget(QLabel("Start #:"))
        format_layout.addWidget(self.start_num_input)

        # File list
        self.file_list_widget = QListWidget()

        # Rename button
        rename_btn = QPushButton("Rename Files")
        rename_btn.clicked.connect(self.rename_files)

        layout.addLayout(folder_layout)
        layout.addLayout(format_layout)
        layout.addWidget(self.file_list_widget)
        layout.addWidget(rename_btn)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def browse_folder(self):
        path = QFileDialog.getExistingDirectory(self, "Select Folder")
        if path:
            self.folder_path = path
            self.folder_label.setText(os.path.basename(path))
            self.load_images()

    def load_images(self):
        self.file_list_widget.clear()
        self.file_list = [f for f in os.listdir(self.folder_path) if is_image_file(f)]
        for f in self.file_list:
            self.file_list_widget.addItem(f)

    def rename_files(self):
        if not self.folder_path:
            QMessageBox.warning(self, "No folder", "Please select a folder first.")
            return

        format_str = self.format_input.text()
        start_num = self.start_num_input.value()

        success, message = rename_photos(self.folder_path, self.file_list, format_str, start_num)
        if success:
            QMessageBox.information(self, "Success", message)
            self.load_images()
        else:
            QMessageBox.critical(self, "Error", message)