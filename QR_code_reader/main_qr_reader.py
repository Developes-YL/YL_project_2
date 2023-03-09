import sys
import cv2
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QMainWindow, QApplication
from imutils import resize
from imutils.video import VideoStream
from pyzbar import pyzbar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.previous_qr_code = ""
        self.camera_on = False
        self.load_ui('Support/main_window.ui')
        self.reset_status()
        self.start_camera()

    def load_ui(self, file_name: str):
        uic.loadUi(file_name, self)

    def update(self, delta: int = 100):
        QTimer.singleShot(delta, self.update)

        qr_code = self.get_text_from_qr()
        if not qr_code:
            self.status.setText("идёт поиск QR-кода")
            return

        self.status.setText("QR-код найден")

        if qr_code == self.previous_qr_code:
            return

        self.reset_status()

        self.previous_qr_code = qr_code
        res = self.recognize_text(qr_code)

        if not res:
            self.status_2.setText("ОШИБКА!")
            return

        status, name, photo = res
        self.update_status(status, name, photo)

    def recognize_text(self, text: str):
        words = text.split(" ")
        if len(words) != 2:
            return False

        code, student_id = words
        res = self.get_inf_from_bot(code, student_id)
        return res

    def start_camera(self):
        try:
            self.vs = VideoStream(src=0).start()
        except:
            sys.exit()
        self.camera_on = True
        self.update()

    def stop_camera(self):
        self.camera_on = False
        self.vs.stop()

    def get_inf_from_bot(self, code, student_id):
        return ["0"] * 3

    def update_status(self, status, name, photo):
        self.about.setText(name)
        self.status.setText(status)

    def reset_status(self):
        self.about.setText("")
        self.status.setText("")
        self.status_2.setText("")

    def get_text_from_qr(self):
        frame = self.vs.read()
        frame = resize(frame, width=400)
        barcodes = pyzbar.decode(frame)
        if not barcodes:
            return None
        for barcode in barcodes:
            if not barcode:
                continue
            barcode_data = barcode.data.decode("utf-8")
            return barcode_data

    def exit(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop_camera()
        super().__exit__(exc_type, exc_val, exc_tb)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())
