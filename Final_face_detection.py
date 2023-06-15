import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget
import cv2
import face_recognition
import datetime
import pandas as pd

class FaceRecognitionApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Attendance System")
        self.setFixedSize(800, 600)

        # Creating GUI elements
        self.image_label = QLabel(self)
        self.capture_button = QPushButton("Capture", self)
        self.capture_button.setEnabled(False)
        self.capture_button.clicked.connect(self.mark_attendance)

        # Creating layout & adding GUI elements
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.capture_button)

        # Creating a central widget & set the layout
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Initializing vars for face recognition 
        self.known_encodings = []
        self.known_names = []

        # Loading known faces & encodings from images
        self.load_known_faces()

        # Open the camera for capturing video
        self.video_capture = cv2.VideoCapture(0)
        self.timer = QTimer()
        self.timer.timeout.connect(self.detect_faces)
        self.timer.start(30)  # frame update in every 30 ms

    def load_known_faces(self):
        # Loading known faces ad ecnodings from images
        known_images = ["images\Rajesh Jaat.png", "images\img.png"] 
        for image_path in known_images:
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            name = image_path.split('\\')[-1].split('.')[0]  # Person name From image path
            self.known_encodings.append(encoding)
            self.known_names.append(name)

    def detect_faces(self):
        ret, frame = self.video_capture.read()
        if not ret:
            return

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(self.known_encodings, face_encoding)
            name = "Unknown" # if not recognized, say "unknown"

            if True in matches:
                match_index = matches.index(True)
                name = self.known_names[match_index]
                self.capture_button.setEnabled(True)

            top, right, bottom, left = face_locations[0]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 1)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 1)

        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setScaledContents(True)

        QApplication.processEvents()

    def mark_attendance(self):
        current_time = datetime.datetime.now()
        day_date = current_time.strftime("%d-%m-%Y")
        time = current_time.strftime("%H:%M:%S")

        # Get the name of the recognized person
        recognized_person = self.known_names[0]

        # Write the attendance to excel file
        df = pd.DataFrame({'Name': [recognized_person], 'Date': [day_date], 'Time': [time]})
        df.to_excel('attendance.xlsx', header=False, index=False)

        # Attendance marked message
        success_message = f"Hey {recognized_person}, Your attendance has been marked."
        self.capture_button.setEnabled(False)
        print(success_message)

    def closeEvent(self, event):
        self.timer.stop()
        self.video_capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FaceRecognitionApp()
    window.show()
    sys.exit(app.exec_())
