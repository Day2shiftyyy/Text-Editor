import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from PyQt5.QtCore import Qt, QTime, QDate
from PyQt5.QtWidgets import QMessageBox, QColorDialog
from PyQt5.QtWidgets import QShortcut
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtGui import QPainter
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5.QtGui import QPixmap, QImage 


class RTE(QMainWindow):
    def __init__(self):
        super(RTE, self).__init__()
        self.editor = QTextEdit()
        self.fontSizeBox = QSpinBox()
        self.exit = QMessageBox()
        QFontDatabase.addApplicationFont("Vanilla Caramel.otf")
        QFontDatabase.addApplicationFont("Spicy Chicken.otf")
        QFontDatabase.addApplicationFont("Country.otf")
        QFontDatabase.addApplicationFont("Coolvetica Compressed hv.otf")
        font = QFont('Vanilla Caramel', 34)
        self.path = ""
        self.editor.setFont(font)
        self.setCentralWidget(self.editor)
        self.showMaximized()
        self.setWindowTitle('Lemickeyy Text Editor')
        self.setWindowIcon(QIcon('logo.jpg'))
        self.painter = QPainter()
        self.tool_bar()
        self.editor.setFontPointSize(34)
        self.shortcut = QShortcut(QKeySequence("Ctrl+s"), self)
        self.shortcut.activated.connect(self.saveFile)
        open_file_action = QAction("Open file", self)
        open_file_action.triggered.connect(self.file_open)
        self.shortcut = QShortcut(QKeySequence("Ctrl+o"), self)
        self.shortcut.activated.connect(self.file_open)
        

    def tool_bar(self):
        toolbar = QToolBar() 

        printbtn = QAction(QIcon('print.ico'), 'Print File', self)
        printbtn.triggered.connect(self.printFile)
        toolbar.addAction(printbtn)
        
        openbtn = QAction(QIcon('open.ico'), 'Open File', self)
        openbtn.triggered.connect(self.file_open)
        toolbar.addAction(openbtn)

        save_action = QAction(QIcon('save.ico'),'Save File', self)
        save_action.triggered.connect(self.saveFile)
        toolbar.addAction(save_action)
         

        undobtn = QAction(QIcon('undo.ico'), 'undo', self)
        undobtn.triggered.connect(self.editor.undo)
        toolbar.addAction(undobtn)


        redobtn = QAction(QIcon('redo.ico'), 'redo', self)
        redobtn.triggered.connect(self.editor.redo)
        toolbar.addAction(redobtn)

        toolbar.addSeparator()

        copybtn = QAction(QIcon('copy.ico'), 'copy', self)
        copybtn.triggered.connect(self.editor.copy)
        toolbar.addAction(copybtn)


        cutbtn = QAction(QIcon('cut.ico'), 'cut', self)
        cutbtn.triggered.connect(self.editor.cut)
        toolbar.addAction(cutbtn)

        pastebtn = QAction(QIcon('paste.ico'), 'paste', self)
        pastebtn.triggered.connect(self.editor.paste)
        toolbar.addAction(pastebtn)

        colorbtn = QAction(QIcon('color.ico'), 'Color', self)
        colorbtn.triggered.connect(self.Color)
        toolbar.addAction(colorbtn)

        toolbar.addSeparator()

        self.fontBox = QComboBox(self)
        self.fontBox.addItems([ "Vanilla Caramel", "Spicy Chicken", "Country", "Coolvetica", "Monospace", "Helvetica"])
        self.fontBox.activated.connect(self.setFont)
        toolbar.addWidget(self.fontBox)

        self.fontSizeBox.setValue(34)
        self.fontSizeBox.valueChanged.connect(self.set_font_size)
        toolbar.addWidget(self.fontSizeBox)

        toolbar.addSeparator()

        rightAllign = QAction(QIcon("right.ico"), "Right Align", self)
        rightAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignRight))
        toolbar.addAction(rightAllign)

        centerAllign = QAction(QIcon("center.ico"), "Center Align", self)
        centerAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignCenter))
        toolbar.addAction(centerAllign)

        leftAllign = QAction(QIcon("left.ico"), "Left Align", self)
        leftAllign.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignLeft))
        toolbar.addAction(leftAllign)

        justify = QAction(QIcon("justify.ico"), "Justify", self)
        justify.triggered.connect(lambda : self.editor.setAlignment(Qt.AlignJustify))
        toolbar.addAction(justify)

        toolbar.addSeparator()

        boldBtn = QAction(QIcon('bold.ico'), 'Bold', self)
        boldBtn.triggered.connect(self.boldText)
        toolbar.addAction(boldBtn)

        underlinebtn = QAction(QIcon('uline.ico'), 'Underline', self)
        underlinebtn.triggered.connect(self.underlineText)
        toolbar.addAction(underlinebtn)

        italicbtn = QAction(QIcon('italic.ico'), 'Italic', self)
        italicbtn.triggered.connect(self.italicText)
        toolbar.addAction(italicbtn)

        toolbar.addSeparator()
        
        timebtn = QAction(QIcon('time.ico'), 'View Time', self)
        timebtn.triggered.connect(self.showTime)
        toolbar.addAction(timebtn)
        
        datebtn = QAction(QIcon('date.ico'), 'View Date', self)
        datebtn.triggered.connect(self.showDate)
        toolbar.addAction(datebtn)

        self.addToolBar(toolbar)  

    def Color(self):
        color = QColorDialog.getColor()
        self.editor.setTextColor(color)

    def set_font_size(self):
        value = self.fontSizeBox.value()
        self.editor.setFontPointSize(value)

    def setFont(self):
        font = self.fontBox.currentText()
        self.editor.setCurrentFont(QFont(font))

    def italicText(self):
        state = self.editor.fontItalic()
        self.editor.setFontItalic(not(state))
    
    def underlineText(self):
        state = self.editor.fontUnderline()
        self.editor.setFontUnderline(not(state))
    
    def boldText(self):
        if self.editor.fontWeight != QFont.Bold:
            self.editor.setFontWeight(QFont.Bold)
            return
        self.editor.setFontWeight(QFont.Normal)
    
    def printFile(self):
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer, self)

        if dialog.exec_() == QPrintDialog.accepted:
            self.editor.print_(printer)
    
        
    def saveFile(self):
        print(self.path)
        if self.path == '':
            self.file_saveas()
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                
        except Exception as e:
            print(e)    
            
    def file_saveas(self):
        self.path, _ = QFileDialog.getSaveFileName(self, "Save file", "", "text documents (*.text);Text documents (*.txt);All files (*.*)")
        if self.path == '':
            return   
        text = self.editor.toPlainText()
        try:
            with open(self.path, 'w') as f:
                f.write(text)
                
        except Exception as e:
            print(e)        
    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "","Text documents (*.txt);All files (*.*)")
        if path:
            try:
                with open(path, 'r') as f:
                    text = f.read()
            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
            
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Quit', 'Did you save the File? If not, click "Cancel." If you do not want to save the file, click "No"',
        QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        if reply == QMessageBox.Yes:
            event.accept()
        elif reply == QMessageBox.No:
            event.accept()
        else:
            event.ignore()

    def showTime(self):
        time = QTime.currentTime()
        self.editor.setText(time.toString(Qt.DefaultLocaleLongDate))
    def showDate(self):
        date = QDate.currentDate()
        self.editor.setText(date.toString(Qt.DefaultLocaleLongDate))

            


app = QApplication(sys.argv)
app.setStyle("Fusion")
palette = QPalette()
palette.setColor(QPalette.Window, Qt.cyan)
palette.setColor(QPalette.WindowText, Qt.black)
palette.setColor(QPalette.Base, QColor(230,230,250))
palette.setColor(QPalette.AlternateBase, QColor(230,230,250))
palette.setColor(QPalette.ToolTipBase, Qt.black)
palette.setColor(QPalette.ToolTipText, Qt.black)
palette.setColor(QPalette.Text, Qt.black)
palette.setColor(QPalette.Button, QColor(230,230,250))
palette.setColor(QPalette.ButtonText, Qt.black)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
window = RTE()
window.show()
sys.exit(app.exec_())