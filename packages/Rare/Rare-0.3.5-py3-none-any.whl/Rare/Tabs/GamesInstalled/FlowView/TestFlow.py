from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *
from legendary.core import LegendaryCore

from Rare.Tabs.GamesInstalled.FlowView.FlowWidget import FlowWidget
from Rare.ext.QtExtensions import FlowLayout


class FlowTest(QScrollArea):
    def __init__(self, core: LegendaryCore):
        super(FlowTest, self).__init__()
        self.core = core
        self.widget = QWidget()
        self.setWidgetResizable(True)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout = FlowLayout()

        for i in self.core.get_installed_list():
            self.layout.addWidget(FlowWidget(core, i))

        self.widget.setLayout(self.layout)
        self.setWidget(self.widget)