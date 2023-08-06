import os
from logging import getLogger

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from legendary.core import LegendaryCore
from legendary.models.game import InstalledGame
from PyQt5 import QtGui
from Rare.utils.RareConfig import IMAGE_DIR

logger = getLogger("FlowWidget")


class ClickableLabel(QLabel):
    clicked = pyqtSignal()

    def __init__(self):
        super(ClickableLabel, self).__init__()


class FlowWidget(QWidget):
    def __init__(self, core: LegendaryCore, game: InstalledGame):
        super(FlowWidget, self).__init__()
        self.layout = QVBoxLayout()
        self.core = core
        self.game = game

        if os.path.exists(f"{IMAGE_DIR}/{game.app_name}/FinalArt.png"):
            pixmap = QPixmap(f"{IMAGE_DIR}/{game.app_name}/FinalArt.png")
        elif os.path.exists(f"{IMAGE_DIR}/{game.app_name}/DieselGameBoxTall.png"):
            pixmap = QPixmap(f"{IMAGE_DIR}/{game.app_name}/DieselGameBoxTall.png")
        elif os.path.exists(f"{IMAGE_DIR}/{game.app_name}/DieselGameBoxLogo.png"):
            pixmap = QPixmap(f"{IMAGE_DIR}/{game.app_name}/DieselGameBoxLogo.png")
        else:
            logger.warning(f"No Image found: {self.game.title}")
            pixmap = None
        if pixmap:
            w=240
            pixmap = pixmap.scaled(w, int(w*4/3))
            self.image = ClickableLabel()
            self.image.setPixmap(pixmap)
            self.layout.addWidget(self.image)
        self.title_label = QLabel(f"<h3>{game.title}</h3>")
        self.title_label.setStyleSheet("""
            QLabel{
               text-align: center;
            }
        """)
        self.title_label.setWordWrap(True)
        self.layout.addWidget(self.title_label)

        self.info_label = QLabel("")
        self.layout.addWidget(self.info_label)

        self.setLayout(self.layout)
        self.setFixedWidth(self.sizeHint().width())


    def mousePressEvent(self, a0) -> None:
        print("test")

    def mouseDoubleClickEvent(self, a0) -> None:
        print("double")

