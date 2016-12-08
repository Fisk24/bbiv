from PyQt4        import uic
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

class Settings(QDialog):
    def __init__(self, parent=None):
        super(Settings, self).__init__(parent)

        self.parent = parent
        self.ui = uic.loadUi("settings.ui", self)

    @staticmethod
    def showSettings(parent=None):
        dialog = Settings(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
