import sys
from PyQt4 import QtGui
import ui.mainWindow

# Main class of application's ui, liberates main() from high level ui management
class trackerGui():
    def __init__(self, dataManager):
        self.app = QtGui.QApplication(sys.argv)
        self.w = ui.mainWindow.mainWindow(dataManager)
        sys.exit(self.app.exec_())
