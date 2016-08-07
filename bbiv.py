#! /usr/bin/python3

import os, sys, re, argparse
from PyQt4 import uic
from PyQt4.QtGui  import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *

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
    <video width="100%" height="100%" controls>
        <source src="file://{video}" type="video/webm">
    </video>
"""

SWF = """<center>
    scale me!
    <object width="1000px" height="1000px">
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
        self.ui.mainView.load(QUrl("http://www.plateinteractive.com/"))
        # VARS
        self.dir   = ""
        self.index = 0
        self.files = []
        self.imgexts = "(\.png|\.jpeg|\.jpg|\.gif)"

        # CONNECTIONS #
        self.nextToolButton.clicked.connect(self.goNext)
        self.prevToolButton.clicked.connect(self.goPrev)

        # MAIN STEPS

        if args.file:
            self.initFolder()

    def initFolder(self):
        self.identifyStartingDirectory()
        self.getFilesFromStartingDirectory()
        self.identifyStartingFileIndex() 
        self.loadMedia(args.file)
        self.ui.nextToolButton.setEnabled(True)
        self.ui.prevToolButton.setEnabled(True)

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
        self.ui.setWindowTitle(item)

    def wrapIndex(self):
        print(len(self.files))
        print(self.index)
        if self.index > len(self.files)-1:
            self.index = 0
        elif self.index < 0:
            self.index = len(self.files)-1

    def identifyStartingDirectory(self):
        self.dir = os.path.dirname(os.path.realpath(args.file))
        print(self.dir)

    def identifyStartingFileIndex(self):
        self.index = self.files.index(args.file)
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
            if os.path.isfile(d+i):
                x.append(d+i)
        self.files = x

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
