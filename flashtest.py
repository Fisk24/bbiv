#! /usr/bin/python3

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from PyQt4.QtWebKit import *
# Create an application
app = QApplication([])
 
# And a window
win = QWidget()
win.setWindowTitle('QWebView Interactive Demo')
 
# And give it a layout
layout = QVBoxLayout()
win.setLayout(layout)
 
# Create and fill a QWebView
view = QWebView()
view.load(QUrl("http://www.addictinggames.com/car-games/moto-x3m-game.jsp"))
# A button to call our JavaScript
button = QPushButton('Set Full Name')
 
# Interact with the HTML page by calling the completeAndReturnName
# function; print its return value to the console
def complete_name():
    frame = view.page().mainFrame()
    print(frame.evaluateJavaScript('completeAndReturnName();'))
 
# Connect 'complete_name' to the button's 'clicked' signal
button.clicked.connect(complete_name)
 
# Add the QWebView and button to the layout
layout.addWidget(view)
layout.addWidget(button)
 
# Show the window and run the app
win.show()
app.exec_()
