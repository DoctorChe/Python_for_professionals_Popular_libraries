#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys

from PIL import ImageDraw, Image
from PIL.ImageQt import ImageQt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QFileDialog, QLabel
from PyQt5.QtGui import QPixmap


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

        self.label = QLabel()
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(300, 300)
        self.setCentralWidget(self.label)

        self.image_path = None

        self.setGeometry(300, 300, 350, 250)
        self.setWindowTitle('Main window')
        self.statusBar().showMessage('Welcome to Image Converter')
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
        self.set_action(self.convert_bw)

    def set_gray(self):
        self.set_action(self.convert_gray)

    def set_negative(self):
        self.set_action(self.convert_negative)

    def set_sepia(self):
        self.set_action(self.convert_sepia)

    def set_action(self, func):
        if self.image_path:

            img = func(self.image_path)

            pixmap = QPixmap.fromImage(img)
            if pixmap.height() > 300 or pixmap.width() > 300:
                pixmap = pixmap.scaled(300, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            self.label.setPixmap(pixmap)

    @staticmethod
    def convert_bw(image_path):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        pix = image.load()

        factor = 50
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = a + b + c
                if S > (((255 + factor) // 2) * 3):
                    a, b, c = 255, 255, 255
                else:
                    a, b, c = 0, 0, 0
                draw.point((i, j), (a, b, c))

        return ImageQt(image.convert('RGBA'))

    @staticmethod
    def convert_gray(image_path):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        pix = image.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c) // 3
                draw.point((i, j), (S, S, S))

        return ImageQt(image.convert('RGBA'))

    @staticmethod
    def convert_negative(image_path):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        pix = image.load()

        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                draw.point((i, j), (255 - a, 255 - b, 255 - c))

        return ImageQt(image.convert('RGBA'))

    @staticmethod
    def convert_sepia(image_path):
        image = Image.open(image_path)
        draw = ImageDraw.Draw(image)
        width, height = image.size
        pix = image.load()

        depth = 30
        for i in range(width):
            for j in range(height):
                a = pix[i, j][0]
                b = pix[i, j][1]
                c = pix[i, j][2]
                S = (a + b + c)
                a = S + depth * 2
                b = S + depth
                c = S
                if a > 255:
                    a = 255
                if b > 255:
                    b = 255
                if c > 255:
                    c = 255
                draw.point((i, j), (a, b, c))

        return ImageQt(image.convert('RGBA'))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())
