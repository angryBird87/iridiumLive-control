#!/usr/bin/python3

import sys
import subprocess
import webbrowser

from PyQt6.QtWidgets import (
    QApplication,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

confFile="/usr/src/gr-iridium/examples/sdrplay-soapy.conf"

backgroundProcess = None
foreGroundProcess = None

def startGrIridiumBackground():
    global backgroundProcess

    if backgroundProcess is None:
        backgroundProcess = subprocess.Popen(f"iridium-extractor -D 4 ${confFile} | /usr/src/iridium-toolkit/iridium-parser.py -p /dev/stdin /dev/stdout | python3 /usr/src/gr-iridium/udp-for-il.py")
    
def startIridiumLive():
    global foreGroundProcess

    if foreGroundProcess is None:
        foreGroundProcess = subprocess.Popen("/usr/local/src/iridiumLive/IridiumLive")
        foreGroundProcess.communicate()
    
    # Open the app in the default browser
    webbrowser.open_new_tab("http://localhost:7777/live")
    

def start():
    startGrIridiumBackground()
    startIridiumLive()

def stop():
    global backgroundProcess, foreGroundProcess

    if backgroundProcess != None:
        backgroundProcess.terminate()
        backgroundProcess = None

    if foreGroundProcess != None:
        foreGroundProcess.terminate()
        foreGroundProcess = None

app = QApplication([])
window = QWidget()
window.resize(240, 240)
window.setWindowTitle("SDRPlay-Treiber-Management")

layout = QVBoxLayout()
startButton = QPushButton("Starten")
startButton.clicked.connect(start)
layout.addWidget(startButton)

stopButton = QPushButton("Stoppen")
stopButton.clicked.connect(stop)
layout.addWidget(stopButton)

window.setLayout(layout)

window.show()

sys.exit(app.exec())