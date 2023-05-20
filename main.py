from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport


class MyWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Блокнот")
        
        self.CentralWidget = QtWidgets.QTextEdit()
        self.setCentralWidget(self.CentralWidget)
        self.settings = QtCore.QSettings("Настройки", "Блокнот")
        
        if self.settings.contains("Окно/Местоположение"):
            self.setGeometry(self.settings.value("Окно/Местоположение"))
        else:
            self.resize(500, 300)
        
        self._createActions()
        self._createMenuBar()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        fileMenu = QtWidgets.QMenu("&File", self)
        menuBar.addMenu(fileMenu)
        fileMenu.addAction(self.newFileAction)
        fileMenu.addAction(self.openAction)
        fileMenu.addAction(self.saveAction)
        fileMenu.addAction(self.savePDFAction)
        fileMenu.addAction(self.exitAction)
        
        
    def _createActions(self):
        self.savePDFAction = QtWidgets.QAction("Save To PDF", self)
        self.savePDFAction.triggered.connect(self.savePDF)
        self.openAction = QtWidgets.QAction("Open", self)
        self.openAction.triggered.connect(self.open)
        self.saveAction = QtWidgets.QAction("Save", self)
        self.saveAction.triggered.connect(self.save)
        self.exitAction = QtWidgets.QAction("Exit", self)
        self.exitAction.triggered.connect(self.exit)
        self.newFileAction = QtWidgets.QAction("New", self)
        self.newFileAction.triggered.connect(self.newFile)
        
    def closeEvent(self, event):
        self.settings.beginGroup("Окно")
        self.settings.setValue("Местоположение", self.geometry())
        self.settings.endGroup()
        
    def savePDF(self):
        printer = QtPrintSupport.QPrinter()
        painter = QtGui.QPainter()
        text = self.CentralWidget.toPlainText()
        painter.begin(printer)
        
        color = QtGui.QColor(QtCore.Qt.black)
        painter.setPen(QtGui.QPen(color))
        painter.setBrush(QtGui.QBrush(color))
        font = QtGui.QFont("Verdana", pointSize=42)
        painter.setFont(font)
        painter.drawText(10, printer.height()//2 - 100, printer.width() - 20, 50, QtCore.Qt.AlignCenter |
                 QtCore.Qt.TextDontClip, text)
        
        painter.end()
    
    def newFile(self):
        self.CentralWidget.clear()
    
    def save(self):
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, "w") as f:
                f.write(self.CentralWidget.toPlainText())
    
    def open(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", "", "Text Files (*.txt)")
        if file_name:
            with open(file_name, "r") as f:
                self.CentralWidget.setText(f.read())
    
    def exit(self):
        exit(0)


if __name__ == "__main__":
    import sys
    
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()
    sys.exit(app.exec_())
