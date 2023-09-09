# pyqt_nko_board.py

"""NOTE: use shift row for aligning other rows"""

import sys, os
from functools import partial
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

basedir = os.path.dirname(__file__)

try:
    from ctypes import windll  # Only exists on Windows.
    myappid = 'com.nkolearner.nkoboard.1'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass

WINDOW_WIDTH = 798
WINDOW_HEIGHT = 300
SCREEN_HEIGHT = 88
KEY_WIDTH = 48
KEY_HEIGHT = 38

layout = {
    "nko": [
        ["\u07F7", "\u07C1", "\u07C2", "\u07C3", "\u07C4", "\u07C5", "\u07C6", "\u07C7", "\u07C8", "\u07C9", "\u07C0", "\u07FA", "=", "Backspace"],
        ["Tab", "\u07D2", "\u07E5", "\u07CB", "\u07D9", "\u07D5", "\u07E6", "\u07CE", "\u07CC", "\u07CF", "\u07D4", "[", "]", "\\"],
        ["Caps", "\u07CA", "\u07DB", "\u07D8", "\u07DD", "\u07DC", "\u07E4", "\u07D6", "\u07DE", "\u07DF", "\u07D1", "\u07F4", "Enter"],
        ["Shift", "\u07E2", "\u07D0", "\u07D7", "\u07CD", "\u07D3", "\u07E3", "\u07E1", "\u07F8", "\u002E", "/", "Shift"],
        ["Ctrl", "Cmd", "Alt", "Space", "Alt", "Cmd", "Ctrl"]
    ],
    "NKO": [
        ["~", "\u07F9", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "Backspace"],
        ["Tab", "\u07F6", "\u07FD", "\u07FA", "\u07DA", "", "\u07E7", "\u2039", "\u203A", "\uFD3E", "\uFD3F", "{", "}", "|"],
        ["Caps", "\u07EE", "\u07EF", "\u07F0", "\u07F1", "\u07F3", "\u07F2", "\u07EB", "\u07EC", "\u07ED", "\u003A", "\u07F5", "Enter"],
        ["Shift", "\u07E7", "\u07EA", "\u07E9", "\u07FE", "\u07E8", "\u07E0", "\u07FF", "\u00AB", "\u00BB", "\u061F", "Shift"],
        ["Ctrl", "Cmd", "Alt", "Space", "Alt", "Cmd", "Ctrl"]
    ],
    "keyCode": [
        ["Backquote", "Digit1", "Digit2", "Digit3", "Digit4", "Digit5", "Digit6", "Digit7", "Digit8", "Digit9", "Digit0", "Minus", "Equal", "Backspace"],
        ["Tab", "KeyQ", "KeyW", "KeyE", "KeyR", "KeyT", "KeyY", "KeyU", "KeyI", "KeyO", "KeyP", "BracketLeft", "BracketRight", "Backslash"],
        ["CapsLock", "KeyA", "KeyS", "KeyD", "KeyF", "KeyG", "KeyH", "KeyJ", "KeyK", "KeyL", "Semicolon", "Quote", "Enter"],
        ["ShiftLeft", "KeyZ", "KeyX", "KeyC", "KeyV", "KeyB", "KeyN", "KeyM", "Comma", "Period", "Slash", "ShiftRight"],
        ["ControlLeft", "CommandLeft", "AltLeft", "Space", "AltRight", "CommandRight", "ControlRight"]
    ]
}

class NkoWindow(QMainWindow):
    """NkoBoard's main window (GUI or view)"""
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NkoBoard")
        self.setFixedSize(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.generalLayout = QVBoxLayout()
        centralWidget = QWidget(self)
        centralWidget.setLayout(self.generalLayout)
        self.setCentralWidget(centralWidget)
        self._createScreen()
        self._createBoard()        

    def _createScreen(self):
        self.screen = QTextEdit()
        self.screen.setLayoutDirection(Qt.LayoutDirection.RightToLeft)
        self.screen.setFontPointSize(14)
        self.screen.setFixedHeight(SCREEN_HEIGHT)
        self.generalLayout.addWidget(self.screen)

    def _createBoard(self):
        self.buttonMap = {}
        boardLayout = QVBoxLayout()
        self.letterChars = [
            '߷', '߁', '߂', '߃', '߄', '߅', '߆', '߇', '߈', '߉', '߀', '-', '=', 
            'ߒ', 'ߥ', 'ߋ', 'ߙ', 'ߕ', 'ߦ', 'ߎ', 'ߌ', 'ߏ', 'ߔ', '[', ']', '\\', 
            'ߊ', 'ߛ', 'ߘ', 'ߝ', 'ߜ', 'ߤ', 'ߖ', 'ߞ', 'ߟ', 'ߑ', 'ߴ', 
            'ߢ', 'ߐ', 'ߗ', 'ߍ', 'ߓ', 'ߣ', 'ߡ', '߸', '.', '/', 
            '~', '߹', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+',
            '߶', '߽', 'ߺ', 'ߚ', '߫', 'ߧ', '‹', '›', '﴾', '﴿', '{', '}', '|',
            '߮', '߯', '߰', '߱', '߳', '߲', '', '߬', '߭', ':', 'ߵ',
            'ߧ', 'ߪ', 'ߩ', '߾', 'ߨ', 'ߠ', '߿', '«', '»', '؟'
        ]
        for row, keys in enumerate(layout['keyCode']):
            rowLayout = QHBoxLayout()
            for col, key in enumerate(keys):
                self.buttonMap[key] = QPushButton(layout['nko'][row][col])
                if key == 'Backspace':
                    self.buttonMap[key].setFixedSize(77, KEY_HEIGHT)
                elif key == 'Tab':
                    self.buttonMap[key].setFixedSize(76, KEY_HEIGHT)
                elif key in ['CapsLock', 'Enter']:
                    self.buttonMap[key].setFixedSize(89, KEY_HEIGHT)
                elif key in ['ShiftLeft', 'ShiftRight']:
                    self.buttonMap[key].setFixedSize(116, KEY_HEIGHT)
                elif key in ['ControlLeft', 'ControlRight']:
                    self.buttonMap[key].setFixedSize(78, KEY_HEIGHT)
                elif key in ['CommandLeft', 'CommandRight', 'AltLeft', 'AltRight']:
                    self.buttonMap[key].setFixedSize(58, KEY_HEIGHT)
                elif key == 'Space':
                    self.buttonMap[key].setFixedSize(355, KEY_HEIGHT)
                else:
                    self.buttonMap[key].setFixedSize(KEY_WIDTH, KEY_HEIGHT)
                rowLayout.addWidget(self.buttonMap[key])
            boardLayout.addLayout(rowLayout)
        self.generalLayout.addLayout(boardLayout)

    def setScreenText(self, text):
        self.screen.setText(text)
        self.screen.setFocus()


class NkoBoard:
    """PyQt Nkoboard's controller class"""
    def __init__(self, view):
        self._view = view
        self.text = ''
        self.layoutMode = 'nko'
        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self):
        for key, button in self._view.buttonMap.items():
            button.clicked.connect(partial(self._onButtonClicked, key))

    def _onButtonClicked(self, key):
        letter = self._view.buttonMap[key].text()
        if letter in self._view.letterChars:
            self.text += letter
            if self.layoutMode == 'NKO':
                self._onShift()
        elif key == 'Space':
            self.text += ' '
        elif key == 'Backspace':
            self.text = self.text[:-1]
        elif key == 'Enter':
            self.text += '\n'
        elif letter == 'Shift':
            self._onShift()
        self._view.setScreenText(self.text)

    def _onShift(self):
        self.layoutMode = 'nko' if self.layoutMode == 'NKO' else 'NKO'
        for row, keyCodes in enumerate(layout["keyCode"]):
            for col, key in enumerate(keyCodes):
                self._view.buttonMap[key].setText(layout[self.layoutMode][row][col]) 


if __name__ == '__main__':
    app = QApplication([])
    app.setWindowIcon(QIcon(os.path.join(basedir, 'nko.ico')))
    window = NkoWindow()
    window.show()
    NkoBoard(view=window)
    sys.exit(app.exec())

