from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QFileDialog, QSlider, QVBoxLayout, QWidget, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PIL import Image
import io

class ImageCompressorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('WebP Image Compressor')

        # Инициализация переменных
        self.original_image = None
        self.compressed_image = None
        self.compression_quality = 75  # Начальное значение для ползунка качества
        self.original_image_label = QLabel(self)
        self.compressed_image_label = QLabel(self)

        # Метки для отображения размеров изображений
        self.original_image_size_label = QLabel(self)
        self.compressed_image_size_label = QLabel(self)

        # Кнопки
        self.open_button = QPushButton('Open Image')
        self.open_button.clicked.connect(self.load_image)

        self.save_button = QPushButton('Save Compressed Image')
        self.save_button.clicked.connect(self.save_image)
        self.save_button.setEnabled(False)

        # Ползунок качества и его отображение
        self.quality_slider = QSlider(Qt.Horizontal)
        self.quality_slider.setMinimum(1)
        self.quality_slider.setMaximum(100)
        self.quality_slider.setValue(self.compression_quality)
        self.quality_slider.valueChanged.connect(self.update_compression)

        self.quality_value_label = QLabel(f'Quality: {self.compression_quality}')
        self.quality_slider.valueChanged.connect(self.update_quality_label)

        # Настройка layout
        layout = QVBoxLayout()

        # Layout для изображений и их размеров
        image_layout = QHBoxLayout()

        original_layout = QVBoxLayout()
        original_layout.addWidget(self.original_image_label)
        original_layout.addWidget(self.original_image_size_label)

        compressed_layout = QVBoxLayout()
        compressed_layout.addWidget(self.compressed_image_label)
        compressed_layout.addWidget(self.compressed_image_size_label)

        image_layout.addLayout(original_layout)
        image_layout.addLayout(compressed_layout)

        layout.addWidget(self.open_button)
        layout.addWidget(self.quality_slider)
        layout.addWidget(self.quality_value_label)
        layout.addLayout(image_layout)
        layout.addWidget(self.save_button)

        # Центральный виджет
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def load_image(self):
        file_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Images (*.png *.jpg *.jpeg *.bmp *.gif)')
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_original_image()
            self.update_compression()

    def display_original_image(self):
        # Показ исходного изображения в QLabel
        self.display_image(self.original_image, self.original_image_label)

        # Отображение размера исходного изображения
        original_image_size = self.calculate_image_size(self.original_image, format=self.original_image.format)
        self.original_image_size_label.setText(f'Size: {original_image_size}')

    def display_compressed_image(self):
        # Показ сжатого изображения в QLabel
        self.display_image(self.compressed_image, self.compressed_image_label)

        # Отображение размера сжатого изображения
        compressed_image_size = self.calculate_image_size(self.compressed_image, format='WEBP')
        self.compressed_image_size_label.setText(f'Size: {compressed_image_size}')

    def display_image(self, image, label):
        # Отображение изображения в QLabel
        image_data = io.BytesIO()
        image.save(image_data, format='PNG')  # Используется PNG для показа в QLabel
        qimage = QPixmap()
        qimage.loadFromData(image_data.getvalue())
        label.setPixmap(qimage)
        label.setScaledContents(True)
        label.setFixedSize(400, 400)

    def update_compression(self):
        if self.original_image:
            self.compression_quality = self.quality_slider.value()
            image_data = io.BytesIO()
            self.original_image.save(image_data, format='WEBP', quality=self.compression_quality)
            compressed_image_data = io.BytesIO(image_data.getvalue())
            self.compressed_image = Image.open(compressed_image_data)

            # Отображение сжатого изображения
            self.display_compressed_image()
            self.save_button.setEnabled(True)

    def update_quality_label(self):
        self.quality_value_label.setText(f'Quality: {self.quality_slider.value()}')

    def calculate_image_size(self, image, format):
        """Вычисляет размер изображения в MiB или KiB в зависимости от формата."""
        image_data = io.BytesIO()
        image.save(image_data, format=format)  # Сохраняем изображение в указанном формате
        size_in_bytes = len(image_data.getvalue())
        
        if size_in_bytes >= 1024 ** 2:
            size_in_mib = size_in_bytes / (1024 ** 2)
            return f'{size_in_mib:.2f} MiB'
        else:
            size_in_kib = size_in_bytes / 1024
            return f'{size_in_kib:.2f} KiB'

    def save_image(self):
        if self.compressed_image:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '', 'WebP Image (*.webp)')
            if file_path:
                self.compressed_image.save(file_path, 'WEBP', quality=self.compression_quality)

if __name__ == '__main__':
    app = QApplication([])
    window = ImageCompressorApp()
    window.show()
    app.exec_()
