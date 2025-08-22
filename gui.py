import sys
import threading
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLabel, QMessageBox
)
from PyQt5.QtGui import QFont, QTextCursor
from PyQt5.QtCore import Qt
import speech_recognition as sr

recognizer = sr.Recognizer()

class SpeechToTextApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🎤 تحويل الصوت إلى نص")
        self.setGeometry(100, 100, 800, 600)
        self.listening = False

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        layout = QVBoxLayout(self.central_widget)

        self.title_label = QLabel("🎤 تطبيق تحويل الصوت إلى نص")
        self.title_label.setFont(QFont("Arial", 20, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.title_label)

        self.text_area = QTextEdit()
        self.text_area.setFont(QFont("Arial", 14))
        self.text_area.setReadOnly(True)
        layout.addWidget(self.text_area)

        self.listen_button = QPushButton("ابدأ الاستماع 🎧")
        self.listen_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.listen_button.setStyleSheet("background-color: #4CAF50; color: white; padding: 10px;")
        self.listen_button.clicked.connect(self.toggle_listening)
        layout.addWidget(self.listen_button)

        self.clear_button = QPushButton("مسح النصوص 🗑️")
        self.clear_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.clear_button.setStyleSheet("background-color: #FFC107; color: black; padding: 10px;")
        self.clear_button.clicked.connect(self.clear_text)
        layout.addWidget(self.clear_button)

        self.exit_button = QPushButton("إغلاق التطبيق ❌")
        self.exit_button.setFont(QFont("Arial", 14, QFont.Bold))
        self.exit_button.setStyleSheet("background-color: #DC3545; color: white; padding: 10px;")
        self.exit_button.clicked.connect(self.close_app)
        layout.addWidget(self.exit_button)

    def toggle_listening(self):
        if not self.listening:
            self.listening = True
            self.listen_button.setText("إيقاف الاستماع ⏹️")
            self.listen_thread = threading.Thread(target=self.start_listening, daemon=True)
            self.listen_thread.start()
        else:
            self.listening = False
            self.listen_button.setText("ابدأ الاستماع 🎧")

    def start_listening(self):
        while self.listening:
            try:
                with sr.Microphone() as source:
                    self.text_area.append("⏳ جاري الاستماع...")
                    QApplication.processEvents()  # تحديث الواجهة
                    recognizer.adjust_for_ambient_noise(source, duration=1)
                    audio = recognizer.listen(source)
                    text = recognizer.recognize_google(audio, language="ar-EG,en-US").lower()
                    self.text_area.append(f"✅ النص المكتشف: {text}\n")
            except sr.UnknownValueError:
                self.text_area.append("❌ لم أتمكن من فهم الصوت، حاول مرة أخرى.\n")
            except sr.RequestError:
                self.text_area.append("⚠️ هناك مشكلة في الاتصال بخدمة التعرف على الصوت.\n")
            self.text_area.moveCursor(QTextCursor.End)

    def clear_text(self):
        self.text_area.clear()


    def close_app(self):
        reply = QMessageBox.question(
            self, "تأكيد الإغلاق", "هل تريد بالتأكيد إغلاق التطبيق؟", QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.listening = False
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpeechToTextApp()
    window.show()
    sys.exit(app.exec_())
