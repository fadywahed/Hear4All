import sys
import os
import speech_recognition as sr
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QScrollArea
from PyQt6.QtGui import QPixmap, QFont, QIcon
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PIL import Image, ImageDraw, ImageFont

r = sr.Recognizer()
image_folder = r"D:\Study\3th Years\Capstone\sign\sign_language_images"
IMAGE_SIZE = (200, 200)

image_cache = {}
for filename in os.listdir(image_folder):
    if filename.endswith(".png"):
        word = os.path.splitext(filename)[0].lower()
        img = Image.open(os.path.join(image_folder, filename)).resize(IMAGE_SIZE, Image.LANCZOS)
        image_cache[word] = img.convert("RGB")

class SpeechRecognitionThread(QThread):
    result_signal = pyqtSignal(list)

    def run(self):
        with sr.Microphone() as src:
            try:
                myaudio = r.listen(src, timeout=3, phrase_time_limit=5)
                mytext = r.recognize_google(myaudio, language="ar-EG").lower()
                words = mytext.split()
                images = []

                for i, word in enumerate(words, start=1):
                    if word in image_cache:
                        img = image_cache[word].copy()


                        draw = ImageDraw.Draw(img)
                        font = ImageFont.truetype("arial.ttf", 40)
                        text = str(i)

                        bbox = draw.textbbox((0, 0), text, font=font)
                        text_width = bbox[2] - bbox[0]
                        text_height = bbox[3] - bbox[1]

                        text_x = (IMAGE_SIZE[0] - text_width) // 2
                        text_y = 10

                        draw.rectangle(
                            [(text_x - 5, text_y - 5),
                             (text_x + text_width + 5, text_y + text_height + 5)],
                            fill="white"
                        )
                        draw.text((text_x, text_y), text, fill="black", font=font)

                        img_path = f"temp_{i}.png"
                        img.save(img_path)
                        images.append(img_path)

                self.result_signal.emit(images)

            except Exception as e:
                self.result_signal.emit([])


class SignLanguageApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🔠 مترجم الإشارة")
        self.setGeometry(200, 200, 1000, 600)
        self.setStyleSheet("background-color: #1e1e2e; color: white; font-size: 16px;")

        title = QLabel("🔠 مترجم الإشارة", self)
        title.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.record_button = QPushButton("🎤 اضغط للتحدث", self)
        self.record_button.setFont(QFont("Arial", 18))
        self.record_button.setIcon(QIcon("mic.png"))
        self.record_button.setStyleSheet(
            "background-color: #0078D7; color: white; border-radius: 10px; padding: 10px;"
        )
        self.record_button.clicked.connect(self.start_speech_recognition)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.image_container = QWidget()
        self.image_layout = QHBoxLayout(self.image_container)
        self.scroll_area.setWidget(self.image_container)

        main_layout = QVBoxLayout()
        main_layout.addWidget(title)
        main_layout.addWidget(self.record_button)
        main_layout.addWidget(self.scroll_area)

        self.setLayout(main_layout)

        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.result_signal.connect(self.display_images)

    def start_speech_recognition(self):
        self.record_button.setText("🎤 جاري الاستماع...")
        self.speech_thread.start()

    def display_images(self, images):
        for i in reversed(range(self.image_layout.count())):
            self.image_layout.itemAt(i).widget().deleteLater()

        if images:
            for img_path in images:
                pixmap = QPixmap(img_path)
                label = QLabel(self)
                label.setPixmap(pixmap)
                label.setScaledContents(True)
                label.setFixedSize(200, 200)
                self.image_layout.addWidget(label)

        self.record_button.setText("🎤 اضغط للتحدث")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SignLanguageApp()
    window.show()
    sys.exit(app.exec())
