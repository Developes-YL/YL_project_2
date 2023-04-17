import base64
import sys
from PyQt5 import uic
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication
from imutils import resize
from imutils.video import VideoStream
from pyzbar import pyzbar

from QR_code_reader import UI_FILE, ACCEPT, REJECT
from QR_code_reader.modules import get_inf_from_bot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.previous_qr_code = ""
        self.camera_on = False
        self.load_ui(UI_FILE)
        font = QFont()
        font.setPointSize(16)
        self.status.setFont(font)
        font.setPointSize(32)
        self.status_2.setFont(font)
        self.about.setFont(font)

        self.reset_status()
        self.start_camera()

    def set_new_photo(self, pixmap: QPixmap):
        try:
            w_old, h_old = pixmap.width(), pixmap.height()
            w_max, h_max = self.image.width(), self.image.height()
            k = max(w_old / w_max, h_old / h_max)
            pixmap = pixmap.scaled(int(w_old / k), int(h_old / k))
            self.image.setPixmap(pixmap)
        except Exception as e:
            print("image error", e.__class__.__name__)

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

        student_id, code = words
        res = get_inf_from_bot(code, student_id)
        if res["ok"]:
            qim = QImage.fromData(base64.b64decode(res["image"]))
            pix = QPixmap.fromImage(qim)
            ans = str(res["status"]), '\n'.join(res["name"].split()) + "\n" + res["grade"], pix
            return ans
        else:
            self.reset_status()
            self.status_2.setText(res["description"])
            return []

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

    def update_status(self, status, name, photo):
        self.about.setText(name)
        self.status_2.setText(status)
        if status == "True":
            self.status_2.setPixmap(QPixmap(ACCEPT).scaled(300, 300))
        else:
            self.status_2.setPixmap(QPixmap(REJECT).scaled(300, 300))
        self.set_new_photo(photo)

    def reset_status(self):
        self.about.setText("")
        self.status.setText("")
        self.status_2.setText("")
        self.image.setPixmap(QPixmap())

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
