
#Copyright (c) 2023 BUG STUDIO. All rights reserved.

import sys
import random
import psutil
import os
import tkinter.messagebox
from PySide6.QtWidgets import QPushButton,QVBoxLayout,QMenu,QSystemTrayIcon,QWidget,QApplication
from PySide6.QtCore import Qt,Slot
from PySide6.QtGui import QAction, QIcon, QKeySequence, QShortcut
from configparser import ConfigParser
import win32gui
def windowEnumerationHandler(hwnd, windowlist):
    windowlist.append((hwnd, win32gui.GetWindowText(hwnd)))
class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.button = QPushButton("Rd")
        self.setWindowTitle("Random")
        self.button.setFixedSize(70,30)
        self.button.setStyleSheet("QPushButton{background-color: rgba(255, 255, 255,50);border-radius: 15px; border: 0.5px groove gray;border-style: outset;font-family: Microsoft YaHei; font-size: 15pt;}"
                                  "QPushButton:hover{background-color: rgba(255, 255, 255,200);border-radius: 15px; border: 0.5px groove gray;border-style: outset;font-family: Microsoft YaHei; font-size: 15pt;}"
                                  "QPushButton:pressed{background-color: rgba(255, 255, 255,200);border-radius: 15px; border: 0.5px groove gray;border-style: outset;font-family: Microsoft YaHei; font-size: 15pt;}")
        self.button.installEventFilter(self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.button)
        self.setLayout(self.layout)
        self.button.clicked.connect(self.magic)
        self._restore_action = QAction()
        self._quit_action = QAction()
        self._tray_icon_menu = QMenu()
        self.tray_icon = QSystemTrayIcon(self)
        if tray_icon==1:
            self.tray_icon.setIcon(QIcon("trayicon_light.png"))
        elif tray_icon==0:
            self.tray_icon.setIcon(QIcon("trayicon_dark.png"))
        self.tray_icon.setToolTip("Random")
        self.create_actions()
        self.create_tray_icon()
        self.tray_icon.show()
        self.tray_icon.activated.connect(self.tray_icon_activated)
        self.listen_keyboard_esc()
        self.listen_keyboard_pgup()
        self.listen_keyboard_pgdown()
        self.listen_keyboard_up()
        self.listen_keyboard_down()
        self.listen_keyboard_enter()
        self.listen_keyboard_left()
        self.listen_keyboard_right()
        self.show()
    def minimize_to_tray(self):
        self.hide()
    def restore_from_tray(self):
        if self.isMinimized():
            self.showNormal()
        elif self.isMaximized():
            self.showMaximized()
        else:
            self.show()
    def about(self):
        os.startfile("About.exe")
    def setting(self):
        os.startfile("config.ini")
    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.restore_from_tray()
    def create_actions(self):
        self._setting_action = QAction("设置", self)
        self._setting_action.triggered.connect(self.setting)
        self._about_action = QAction("关于", self)
        self._about_action.triggered.connect(self.about)
        self._hide_action = QAction("隐藏", self)
        self._hide_action.triggered.connect(self.minimize_to_tray)
        self._restore_action = QAction("显示", self)
        self._restore_action.triggered.connect(self.restore_from_tray)
        self._quit_action = QAction("退出", self)
        self._quit_action.triggered.connect(QApplication.quit)
    def create_tray_icon(self):
        self._tray_icon_menu = QMenu(self)
        self._tray_icon_menu.addAction(self._setting_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._about_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._hide_action)
        self._tray_icon_menu.addAction(self._restore_action)
        self._tray_icon_menu.addSeparator()
        self._tray_icon_menu.addAction(self._quit_action)
        self.tray_icon.setContextMenu(self._tray_icon_menu)
        self.tray_icon.show()
    def listen_keyboard_esc(self):
        shortcut = QShortcut(QKeySequence("Esc"), self)
        shortcut.activated.connect(self.hide)
    def listen_keyboard_pgup(self):
        shortcut = QShortcut(QKeySequence("PgUp"), self)
        shortcut.activated.connect(self.magic)
    def listen_keyboard_pgdown(self):
        shortcut = QShortcut(QKeySequence("PgDown"), self)
        shortcut.activated.connect(self.magic)
    def listen_keyboard_up(self):
        shortcut = QShortcut(QKeySequence("Up"), self)
        shortcut.activated.connect(self.magic)
    def listen_keyboard_down(self):
        shortcut = QShortcut(QKeySequence("Down"), self)
        shortcut.activated.connect(self.magic)
    def listen_keyboard_enter(self):
        shortcut = QShortcut(QKeySequence("Enter"), self)
        shortcut.activated.connect(self.magic)
    def listen_keyboard_left(self):
        shortcut = QShortcut(QKeySequence("Left"), self)
        shortcut.activated.connect(self.magic)
    def listen_keyboard_right(self):
        shortcut = QShortcut(QKeySequence("Right"), self)
        shortcut.activated.connect(self.magic)
    @Slot()
    def magic(self):
        global arr
        temp=random.choice(arr)
        self.button.setText(str(temp))
        arr.remove(temp)
        windowlist = []
        win32gui.EnumWindows(windowEnumerationHandler, windowlist)
        for i in windowlist:
            if "幻灯片放映" in i[1].lower():
                win32gui.ShowWindow(i[0],4)
                win32gui.SetForegroundWindow(i[0])
                break
        if not arr:
            arr=[x for x in range(1,value+1)]
if __name__ == "__main__":
    conf = ConfigParser()
    conf.read('config.ini')
    position_x=int(conf['window']['position_x'])
    position_y=int(conf['window']['position_y'])
    tray_icon=int(conf['window']['tray_icon'])
    value=int(conf['random']['value'])
    arr=[x for x in range(1,value+1)]
    app = QApplication(sys.argv)
    widget = Widget()
    widget.resize(0,0)
    widget.move(position_x,position_y)
    widget.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool)
    widget.setAttribute(Qt.WA_TranslucentBackground)
    widget.activateWindow()
    widget.show()
    sys.exit(app.exec())
