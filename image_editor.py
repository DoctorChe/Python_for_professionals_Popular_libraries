import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap

from utils import edit, database

TEMP_FILE = 'temp.jpg'


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.initUI()

    def initUI(self):
        open_action = QAction('&Open Image', self)
        open_action.setShortcut('Ctrl+O')
        open_action.setStatusTip('Open Image')
        open_action.triggered.connect(self.open_image)

        save_action = QAction('&Save Image', self)
        save_action.setShortcut('Ctrl+S')
        save_action.setStatusTip('Save Image')
        save_action.triggered.connect(self.save_image)

        close_action = QAction('E&xit', self)
        close_action.setShortcut('Ctrl+Q')
        close_action.setStatusTip('Exit')
        close_action.triggered.connect(self.close)

        bw_action = QAction('&BW', self)
        bw_action.setShortcut('Ctrl+B')
        bw_action.setStatusTip('Convert image to BW')
        bw_action.triggered.connect(self.set_bw)

        gray_action = QAction('&Gray', self)
        gray_action.setShortcut('Ctrl+G')
        gray_action.setStatusTip('Convert image to Gray')
        gray_action.triggered.connect(self.set_gray)

        negative_action = QAction('&Negative', self)
        negative_action.setShortcut('Ctrl+N')
        negative_action.setStatusTip('Convert image to Negative')
        negative_action.triggered.connect(self.set_negative)

        sepia_action = QAction('&Sepia', self)
        sepia_action.setShortcut('Ctrl+S')
        sepia_action.setStatusTip('Convert image to Sepia')
        sepia_action.triggered.connect(self.set_sepia)

        crop_action = QAction('&Crop', self)
        crop_action.setStatusTip('Crop image')
        crop_action.triggered.connect(self.set_crop)

        scale_0_25_action = QAction('Scale x0.25', self)
        scale_0_25_action.setStatusTip('Scale image x0.25')
        scale_0_25_action.triggered.connect(lambda: self.set_scale(0.25))

        scale_0_5_action = QAction('Scale x0.5', self)
        scale_0_5_action.setStatusTip('Scale image x0.5')
        scale_0_5_action.triggered.connect(lambda: self.set_scale(0.5))

        scale_0_75_action = QAction('Scale x0.75', self)
        scale_0_75_action.setStatusTip('Scale image x0.75')
        scale_0_75_action.triggered.connect(lambda: self.set_scale(0.75))

        scale_1_25_action = QAction('Scale x1.25', self)
        scale_1_25_action.setStatusTip('Scale image x1.25')
        scale_1_25_action.triggered.connect(lambda: self.set_scale(1.25))

        scale_1_5_action = QAction('Scale x1.5', self)
        scale_1_5_action.setStatusTip('Scale image x1.5')
        scale_1_5_action.triggered.connect(lambda: self.set_scale(1.5))

        scale_1_75_action = QAction('Scale x1.75', self)
        scale_1_75_action.setStatusTip('Scale image x1.75')
        scale_1_75_action.triggered.connect(lambda: self.set_scale(1.75))

        scale_2_0_action = QAction('Scale x2', self)
        scale_2_0_action.setStatusTip('Scale image x2')
        scale_2_0_action.triggered.connect(lambda: self.set_scale(2.0))

        save_to_db_action = QAction('Save to DB', self)
        save_to_db_action.setStatusTip('Save image to DB')
        save_to_db_action.triggered.connect(self.set_save_to_db)

        menubar = self.menuBar()
        file_menu = menubar.addMenu('&File')
        file_menu.addAction(open_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()
        file_menu.addAction(close_action)
        edit_menu = menubar.addMenu('&Edit')
        edit_menu.addAction(bw_action)
        edit_menu.addAction(gray_action)
        edit_menu.addAction(negative_action)
        edit_menu.addAction(sepia_action)
        edit_menu.addSeparator()
        edit_menu.addAction(crop_action)
        scale_menu = edit_menu.addMenu('Scale')
        scale_menu.addAction(scale_0_25_action)
        scale_menu.addAction(scale_0_5_action)
        scale_menu.addAction(scale_0_75_action)
        scale_menu.addAction(scale_1_25_action)
        scale_menu.addAction(scale_1_5_action)
        scale_menu.addAction(scale_1_75_action)
        scale_menu.addAction(scale_2_0_action)
        utils_menu = menubar.addMenu('Utils')
        utils_menu.addAction(save_to_db_action)

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(300, 300)
        self.setCentralWidget(self.label)

        self.image_path = None

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Image Editor')
        self.statusBar().showMessage('Welcome to Image Editor')
        self.show()

    def open_image(self):
        options = QFileDialog.Options()
        self.image_path, _ = QFileDialog.getOpenFileName(self, 'Open Image', '', 'Image Files (*.png *.jpg *.bmp)',
                                                         options=options)
        if self.image_path:
            pixmap = QPixmap(self.image_path)
            if pixmap.height() > 300 or pixmap.width() > 300:
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)

    def save_image(self):
        options = QFileDialog.Options()
        save_image_path, _ = QFileDialog.getSaveFileName(self, 'Save Image', '',
                                                         "Image Files (*.png *.jpg *.bmp)",
                                                         options=options)
        file_format = save_image_path[-3:]
        if save_image_path and file_format in ['png', 'jpg', 'bmp']:
            pixmap = self.label.pixmap()
            pixmap.save(save_image_path, file_format, -1)

    def set_bw(self):
        self.set_action(edit.convert_bw)

    def set_gray(self):
        self.set_action(edit.convert_gray)

    def set_negative(self):
        self.set_action(edit.convert_negative)

    def set_sepia(self):
        self.set_action(edit.convert_sepia)

    def set_crop(self):
        self.set_action(edit.crop)

    def set_scale(self, magnitude):
        self.set_action(edit.scale, magnitude=magnitude)

    def set_action(self, func, **kwargs):
        if self.image_path:

            img = func(self.image_path, **kwargs)

            pixmap = QPixmap.fromImage(img)
            if pixmap.height() > 300 or pixmap.width() > 300:
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)

    def set_save_to_db(self):
        pixmap = self.label.pixmap()
        if pixmap:
            pixmap.save(TEMP_FILE, TEMP_FILE[-3:], -1)
            database.save_to_db(TEMP_FILE)
            try:
                os.remove(TEMP_FILE)
            except IOError:
                pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
