import sys

import requests
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMainWindow, QApplication
from imutils import resize
from imutils.video import VideoStream
from pyzbar import pyzbar

from QR_code_reader.Support.variables import CODE_FILE, HOST, PORT


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.previous_qr_code = ""
        self.camera_on = False
        self.load_ui('Support/main_window.ui')

        self.reset_status()
        self.get_inf_from_bot("0", "")
        # self.start_camera()

    def set_new_photo(self, image: QPixmap):
        pixmap = image.copy()
        w_old, h_old = pixmap.width(), pixmap.height()
        w_max, h_max = self.image.width(), self.image.height()
        k = max(w_old / w_max, h_old / h_max)
        pixmap = pixmap.scaled(int(w_old / k), int(h_old / k))
        self.image.setPixmap(pixmap)

    def load_ui(self, file_name: str):
        uic.loadUi(file_name, self)
        self.showMaximized()

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
        with open(file="Support/CODE.txt", mode="r", encoding="utf-8") as f:
            current_code = f.readline()
        params = {"code": str(hash(current_code)),
                  "id": student_id}
        res = requests.get(f"http://{HOST}:{PORT}/get_photo", params=params).json()
        self.width()
        return [0, 0, res["photo"]]

    def update_status(self, status, name, photo):
        self.about.setText(name)
        self.status.setText(status)
        self.set_new_photo(photo)

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
