import os
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from pathlib import Path
from configparser import ConfigParser
import ctypes

filename1 = ""
filename2 = ""
filekey = ""
folderpath = ""


myappid = 'arodos.opt'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)  # Show icon on taskbar


#region Config
config = ConfigParser()
if Path("config.ini").is_file() == False or os.path.getsize("config.ini") == 0:
    config["settings"] = {
        "keyname": "enc.key",
        "fileformat": "File",
        "filepath": ""
    }
    with open("config.ini", "w") as configfile:
        config.write(configfile)
#endregion


#region OTP           (copied from video)
# Make files the same length
def equalize(path_1, path_2):
    data1 = open(path_1, "rb").read()
    data2 = open(path_2, "rb").read()
    l_data1 = len(data1)
    l_data2 = len(data2)
    if l_data1 > l_data2:
        data2 += os.urandom(l_data1 - l_data2)
    else:
        data1 += os.urandom(l_data2 - l_data1)
    with open(path_1, "wb") as out:
        out.write(data1)
    with open(path_2, "wb") as out:
        out.write(data2)

# generate key
def keygen(orig_path, enc_path, key_path):
    equalize(orig_path, enc_path)
    original = open(orig_path, "rb").read()
    encrypted = open(enc_path, "rb").read()
    key = bytes(a ^ b for (a, b) in zip(original, encrypted))
    with open(key_path + "enc.key", "wb") as key_out:
        key_out.write(key)

# decrypt
def decrypt(enc_path, key_path, dec_path):
    encrypted = open(enc_path, "rb").read()
    key = open(key_path, "rb").read()
    decrypted = bytes(a ^ b for (a, b) in zip(encrypted, key))
    with open(dec_path, "wb") as decrypted_out:
        decrypted_out.write(decrypted)
#endregion

#region GUI
class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.initMe()


    def initMe(self):
        config = ConfigParser()
        config.read('config.ini')
        #region GUI Widgets
        btnWidth = 135
        btnHeight = 23
        # Button file 1
        self.buttonD1 = QPushButton("Select file 1", self)                              #   Type
        self.buttonD1.setGeometry(20,10, btnWidth, btnHeight)                           #   Geometry
        self.buttonD1.clicked.connect(self.btn1)                                        #   Function
        self.buttonD1.setCursor(QCursor(QtCore.Qt.PointingHandCursor))                  #   Coursor "Pointer"
        self.buttonD1.setToolTip("First file for encryption")                           #   Toottip

        # Button file 2
        self.buttonD2 = QPushButton("Select file 2", self)
        self.buttonD2.setGeometry(20, 40, btnWidth, btnHeight)
        self.buttonD2.clicked.connect(self.btn2)
        self.buttonD2.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonD2.setToolTip("Second file for encryption")

        # Button key file
        self.buttonKeyfile = QPushButton("Select key", self)
        self.buttonKeyfile.setGeometry(200, 40, btnWidth, btnHeight)
        self.buttonKeyfile.clicked.connect(self.btnKeyfile)
        self.buttonKeyfile.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonKeyfile.setToolTip("Select key file")

        # Button file 3
        self.buttonD3 = QPushButton("Select file", self)
        self.buttonD3.setGeometry(200, 10, btnWidth, btnHeight)
        self.buttonD3.clicked.connect(self.btn3)
        self.buttonD3.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.buttonD3.setToolTip("File for decryption")

        # Button Key
        self.buttonKey = QPushButton("Generate key", self)
        self.buttonKey.setGeometry(20, 120, btnWidth, btnHeight)
        self.buttonKey.clicked.connect(self.btnKey)
        self.buttonKey.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Out File Combobox
        self.comboFileformat = QComboBox(self)
        self.comboFileformat.setGeometry(200, 80, btnWidth, btnHeight)
        #self.comboFileformat.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.comboFileformat.addItems(["File", ".pdf", ".txt", ".doc", ".docx", ".bmp", ".jpg", ".png", ".gif", ".ppt", ".pptx", ".mp3", ".mp4", ".wav"])
        self.comboFileformat.currentIndexChanged.connect(self.selectionFileformat)
        self.comboFileformat.setCurrentText(config['settings']['fileformat'])
        self.comboFileformat.setToolTip("File format for output file")

        # Out Path Button
        self.buttonOut = QPushButton("Generate output file", self)
        self.buttonOut.setGeometry(200, 120, btnWidth, btnHeight)
        self.buttonOut.clicked.connect(self.btnOut)
        self.buttonOut.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Button Path
        self.buttonPath = QPushButton("Select output path", self)
        self.buttonPath.setGeometry(20, 80, btnWidth, btnHeight)
        self.buttonPath.clicked.connect(self.btnPath)
        self.buttonPath.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        # Label Output
        self.labelOut = QLabel("", self)
        self.labelOut.setFixedSize(200, 15)
        self.labelOut.move(140, 160)

        self.setFixedSize(360,160)                          # Windowsize
        self.setWindowTitle("OTP Encryption")               # Title
        self.setWindowIcon(QIcon("icon.png"))               # Icon
        self.show()
        #endregion


# Functions
    def btn1(self):
        fd = QFileDialog()
        fName = fd.getOpenFileName(self, "Select file")
        global filename1
        filename1 = fName[0]
        self.buttonD1.setText(os.path.basename(fName[0]))

    def btn2(self):
        fd = QFileDialog()
        fName = fd.getOpenFileName(self, "Select file")
        global filename2
        filename2 = fName[0]
        self.buttonD2.setText(os.path.basename(fName[0]))

    def btn3(self):
        fd = QFileDialog()
        fName = fd.getOpenFileName(self, "Select file")
        global filename3
        filename3 = fName[0]
        self.buttonD3.setText(os.path.basename(fName[0]))

    def btnKeyfile(self):
        fd = QFileDialog()
        fName = fd.getOpenFileName(self, "Select key")
        global filekey
        filekey = fName[0]
        self.buttonKeyfile.setText(os.path.basename(fName[0]))

    def btnKey(self):
        global filename1, filename2
        fileObj1 = Path(filename1)
        fileObj2 = Path(filename2)
        config = ConfigParser()
        config.read('config.ini')

        if fileObj1.is_file() == True and fileObj2.is_file() == True:
            keygen(filename1, filename2, config['settings']['filepath'])
            self.labelOut.setText("Key generated successfully")
        else:
            self.labelOut.setText("File path not correct")

    def btnOut(self):
        global filename3, filekey
        fileObj1 = Path(filename3)
        fileObj2 = Path(filekey)
        config = ConfigParser()
        config.read('config.ini')
        if self.comboFileformat.currentIndex() == 0:
            end = ""
        else:
            end = self.comboFileformat.currentText()

        if fileObj1.is_file() == True and fileObj2.is_file() == True:
            decrypt(filename3, filekey, config['settings']['filepath'] + "out" + end)
            self.labelOut.setText("Output file generated successfully")
        else:
            self.labelOut.setText("File path not correct")

    def selectionFileformat(self):
        config = ConfigParser()
        config.read('config.ini')
        config["settings"] = {
            "keyname": config['settings']['keyname'],
            "fileformat": self.comboFileformat.currentText(),
            "filepath": config['settings']['filepath']
        }
        with open("config.ini", "w") as configfile:
            config.write(configfile)

    def btnPath(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        global folderpath
        folderpath = folder
        self.buttonPath.setText(folder)

        config = ConfigParser()
        config.read('config.ini')
        config["settings"] = {
            "keyname": config['settings']['keyname'],
            "fileformat": config['settings']['fileformat'],
            "filepath": folderpath
        }
        with open("config.ini", "w") as configfile:
            config.write(configfile)

app = QApplication(sys.argv)
w = Window()
sys.exit(app.exec_())
#endregion