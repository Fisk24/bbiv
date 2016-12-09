#! /usr/bin/python3

import os, sys, re, argparse
from PyQt4 import uic
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

from settings import Settings

HEAD = """<head>
    <style>
        div.image img {
            margin: 0;
            background: yellow;
            position: absolute;
            top: 50%;
            left: 50%;
            margin-right: -50%;
            transform: translate(-50%, -50%) } 

        div.vid video {
            margin: 0;
            background: yellow;
            position: absolute;
            top: 50%;
            left: 50%;
            margin-right: -50%;
            transform: translate(-50%, -50%) }
    </style>
</head>
"""

WEBM = """
    <video width="100%" height="100%" autoplay loop>
        <source src="file://{video}" type="video/webm">
    </video>
"""

SWF = """<center>
    scale me!
    <object width="100%" height="100%">
        <param name="movie" value="file://{flash}" />
	<param name="quality" value="high" />
	<PARAM NAME="SCALE" VALUE="exactfit" />
        <embed src="file://{flash}" quality="high" type="application/x-shockwave-flash" width="100%" height="100%" SCALE="exactfit" pluginspage="http://www.macromedia.com/go/getflashplayer" />
    </object>
</center>
"""

IMG = """<center>
    <img style="width:auto; height:95%;" src="{image}"/>
</center>
"""

parser = argparse.ArgumentParser()
parser.add_argument("--file", "-f", help="Specifies the file to displayed.")

args = parser.parse_args()

class Main(QMainWindow):
    def __init__(self):
        super(Main, self).__init__()

        ### LOAD UI FILES ###
        self.ui = uic.loadUi("./main.ui", self)
        self.ui.mainView.settings().setAttribute(QWebSettings.PluginsEnabled, True)
        #self.ui.mainView.load(QUrl("http://www.plateinteractive.com/")) # Flash test...
        # VARS
        self.dir   = ""
        self.index = 0
        self.files = []
        self.supported = "(\.png|\.jpeg|\.jpg|\.gif|\.swf|\.webm)"
        self.imgexts = "(\.png|\.jpeg|\.jpg|\.gif)"

        # CONNECTIONS #
        self.nextToolButton.clicked.connect(self.goNext)
        self.prevToolButton.clicked.connect(self.goPrev)
        self.openToolButton.clicked.connect(self.openSupportedFile)
        self.settToolButton.clicked.connect(self.editSettings)

        self.rSidePrev.clicked.connect(self.goPrev)
        self.rSideNext.clicked.connect(self.goNext)
        self.rSideOpen.clicked.connect(self.openSupportedFile)
        self.rSideSettings.clicked.connect(self.editSettings)

        self.lSidePrev.clicked.connect(self.goPrev)
        self.lSideNext.clicked.connect(self.goNext)
        self.lSideOpen.clicked.connect(self.openSupportedFile)
        self.lSideSettings.clicked.connect(self.editSettings)

        # MAIN STEPS
        self.setInitialWindowTitle()
        self.setLayoutRighty()

        if args.file:
            if os.path.isfile(args.file):
                self.initFile()
            elif os.path.isdir(args.file):
                self.initFolder()

    def editSettings(self):
        Settings.showSettings(self)

    def openSupportedFile(self):
        file_string = QFileDialog.getOpenFileName(self)
        if file_string:
            self.identifyStartingDirectory(file_string)
            self.getFilesFromStartingDirectory()
            self.identifyStartingFileIndex(file_string) 
            self.loadMedia(file_string)
            self.ui.nextToolButton.setEnabled(True)
            self.ui.prevToolButton.setEnabled(True)
            self.ui.sideNextToolButton.setEnabled(True)
            self.ui.sidePrevToolButton.setEnabled(True)
            self.ui.rSideNext.setEnabled(True)
            self.ui.rSidePrev.setEnabled(True)
            self.ui.lSideNext.setEnabled(True)
            self.ui.lSidePrev.setEnabled(True)

    def initFile(self):
        self.identifyStartingDirectory()
        self.getFilesFromStartingDirectory()
        self.identifyStartingFileIndex() 
        self.loadMedia(args.file)
        self.ui.nextToolButton.setEnabled(True)
        self.ui.prevToolButton.setEnabled(True)
        self.ui.sideNextToolButton.setEnabled(True)
        self.ui.sidePrevToolButton.setEnabled(True)
        self.ui.rSideNext.setEnabled(True)
        self.ui.rSidePrev.setEnabled(True)
        self.ui.lSideNext.setEnabled(True)
        self.ui.lSidePrev.setEnabled(True)

    def initFolder(self):
        self.identifyStartingDirectory()
        self.getFilesFromStartingDirectory()
        self.index = 0
        self.loadMedia(self.files[0])
        self.ui.nextToolButton.setEnabled(True)
        self.ui.prevToolButton.setEnabled(True)
        self.ui.sideNextToolButton.setEnabled(True)
        self.ui.sidePrevToolButton.setEnabled(True)
        self.ui.rSideNext.setEnabled(True)
        self.ui.rSidePrev.setEnabled(True)
        self.ui.lSideNext.setEnabled(True)
        self.ui.lSidePrev.setEnabled(True)

    def setLayoutRighty(self):
        # Enable this layout
        self.ui.rSideNext.setVisible(True)
        self.ui.rSidePrev.setVisible(True)
        self.ui.rSideOpen.setVisible(True)
        self.ui.rSideShuffle.setVisible(True)
        self.ui.rSideFullscreen.setVisible(True)
        self.ui.rSideSettings.setVisible(True)
        # Disable all other
        self.ui.lSideNext.setVisible(False)
        self.ui.lSidePrev.setVisible(False)
        self.ui.lSideOpen.setVisible(False)
        self.ui.lSideShuffle.setVisible(False)
        self.ui.lSideFullscreen.setVisible(False)
        self.ui.lSideSettings.setVisible(False)

        self.ui.prevToolButton.setVisible(False)
        self.ui.nextToolButton.setVisible(False)
        self.ui.openToolButton.setVisible(False)
        self.ui.settToolButton.setVisible(False)
        self.ui.fullToolButton.setVisible(False)
        self.ui.shufToolButton.setVisible(False)

        self.ui.sidePrevToolButton.setVisible(False)
        self.ui.sideNextToolButton.setVisible(False)

    def goNext(self):
        self.index += 1
        self.wrapIndex() 
        item = self.files[self.index]

        self.loadMedia(item)
        self.ui.statusbar.showMessage(item, 2000)
        self.ui.setWindowTitle("{i}: {n}".format(i=self.index, n=item))

    def goPrev(self):
        self.index -= 1
        self.wrapIndex()
        item = self.files[self.index]

        self.loadMedia(item)
        self.ui.statusbar.showMessage(item, 2000)
        self.ui.setWindowTitle("{i}: {n}".format(i=self.index, n=item))

    def wrapIndex(self):
        #print(len(self.files))
        #print(self.index)
        if self.index > len(self.files)-1:
            self.index = 0
        elif self.index < 0:
            self.index = len(self.files)-1

    def identifyStartingDirectory(self, file=args.file):
        if os.path.isfile(file):
            self.dir = os.path.dirname(os.path.realpath(file))
            print(self.dir)
        else:
            self.dir = file

    def identifyStartingFileIndex(self, file=args.file):
        self.index = self.files.index(file)
        print(self.index)

    def loadMedia(self, uri):
        # This function is designed to be called directly to change the QWebView to a specified file
        if re.search(self.imgexts, uri, re.IGNORECASE):
            self.assembleIndex(IMG, image=uri)
        elif re.search("\.swf", uri, re.IGNORECASE):
            self.assembleIndex(SWF, flash=uri)
        elif re.search("\.webm", uri, re.IGNORECASE):
            self.assembleIndex(WEBM, uri, re.IGNORECASE)
        else:
            self.assembleIndex("Unsuported file type :C")

        self.ui.mainView.load(QUrl("index.html"))
    
    def assembleIndex(self, block, video="", image="", flash="", head=""):
        html = head+block.format(image=image, video=video, flash=flash)
        #print(html)
        with open("index.html", 'w') as page:
            page.write(html)

    def getFilesFromStartingDirectory(self):
        # itterate through the given directory adding every thing thats not a folder to a list then return that list
        d = self.dir+"/"
        x = []
        for i in os.listdir(d):
            if re.search(self.supported, i) and os.path.isfile(d+i):
                x.append(d+i)
        self.files = x

    def setInitialWindowTitle(self):
        # this function will set the window title when the application starts
        pass

    def showFiles(self):
        for i in self.files:
            print(i)

if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        win = Main()
        win.show()
        sys.exit(app.exec_())
    except Exception as e:
        raise e
