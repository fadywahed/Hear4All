import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QTextEdit, QPushButton, QHBoxLayout
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import os

class TextToSpeechApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("🗣️ تحويل النص إلى كلام - عربي")
        self.setGeometry(200, 200, 500, 300)

        layout = QVBoxLayout()

        self.label = QLabel("اكتب النص العربي هنا:")
        self.label.setFont(QFont("Arial", 14))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.text_edit = QTextEdit()
        self.text_edit.setFont(QFont("Arial", 14))

        # زر النطق
        self.speak_button = QPushButton("🔊 نطق النص")
        self.speak_button.setFont(QFont("Arial", 14))
        self.speak_button.clicked.connect(self.speak_text)

        # زر المسح
        self.clear_button = QPushButton("🗑️ مسح النص")
        self.clear_button.setFont(QFont("Arial", 14))
        self.clear_button.clicked.connect(self.clear_text)

        # تخطيط أفقي للأزرار (مبادلة الأماكن: زر النطق على اليمين، المسح على الشمال)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.speak_button)

        layout.addWidget(self.label)
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def speak_text(self):
        text = self.text_edit.toPlainText().strip()
        if text:
            tts = gTTS(text=text, lang='ar')
            tts.save("output.mp3")

            # تحميل الصوت وتسريعه
            sound = AudioSegment.from_file("output.mp3", format="mp3")
            faster_sound = sound.speedup(playback_speed=1.5)
            play(faster_sound)

            os.remove("output.mp3")

    def clear_text(self):
        self.text_edit.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TextToSpeechApp()
    window.show()
    sys.exit(app.exec())
