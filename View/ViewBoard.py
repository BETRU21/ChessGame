from typing import NamedTuple
from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QIcon
from PyQt5.Qt import QPixmap
from PyQt5 import QtGui
from PyQt5 import uic
import os

MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '/ui{}BoardWindow.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)

class ViewBoard(QWidget, Ui_MainWindow):
    def __init__(self, dataBoard=None, dicoAndList=None):
        super(ViewBoard, self).__init__()
        self.setupUi(self)
        self.colorTurn = "white"
        self.buttons = {}
        self.dico = dicoAndList.dico
        self.positionsBlack = dicoAndList.positionsBlack
        self.positionsWhite = dicoAndList.positionsWhite
        self.positions = dicoAndList.positions
        self.pieces = dicoAndList.pieces
        self.cmbList = {"white": self.cmb_white, "black": self.cmb_black}
        self.movements = []
        self.selectedPiece = ()
        self.dataBoard = dataBoard
        self.capturedPiecesWhite = []
        self.capturedPiecesBlack = []
        self.buttonPressed = False
        self.createButtonsList()
        self.connectWidgets()
        self.initializeGame()

    def connectWidgets(self):
        size = QSize(40, 40)
        self.cmb_white.setIconSize(size)
        self.cmb_black.setIconSize(size)
        for pos in self.positions:
            pb = self.buttons.get(pos)
            pb.pressed.connect(self.buttonAction)

    def buttonAction(self):
        sender = self.sender().text()
        if self.dataBoard.lookSpecificPosition(sender) == ("empty", "empty"):
            if len(self.movements) == 0:
                pb = self.buttons.get(sender)
                pb.setStatus(False)
                return False
        if sender in self.movements:
            oldPos = self.selectedPiece.get("oldPos")
            color = self.selectedPiece.get("color")
            piece = self.selectedPiece.get("piece")
            promotedPiece = self.cmbList[color].currentText()
            if promotedPiece == "":
                promotedPiece = "pawn"
            move = self.dataBoard.moveItemInGameState(oldPos, sender, color, piece, promotedPiece)
            self.movePiece(oldPos, sender, color, piece)
            self.enableAllButtons()
            self.resetMovements()
            self.buttonPressed = False
            self.selectedPiece = {}
            oldPb = self.buttons.get(oldPos)
            oldPb.setStatus(False)
            pb = self.buttons.get(sender)
            pb.setStatus(False)
            if move.tag == "littleCastling":
                if color == "white":
                    removePos = "h1"
                if color == "black":
                    removePos = "h8"
                self.addPiece(removePos, "empty", "empty")
            if move.tag == "bigCastling":
                if color == "white":
                    removePos = "a1"
                if color == "black":
                    removePos = "a8"
                self.addPiece(removePos, "empty", "empty")
            if move.tag == "passing":
                if color == "white":
                    removePos = move.pos[0] + str(int(move.pos[1]) - 1)
                if color == "black":
                    removePos = move.pos[0] + str(int(move.pos[1]) + 1)
                self.addPiece(removePos, "empty", "empty")
                self.updateCMB()
            if move.tag == "promotion":
                self.reupdateCMB(color)
                self.updateCMB()
            elif move.tag == "promotionAndCapture":
                self.reupdateCMB(color)
                self.updateCMB()
            else:    
                self.updateCMB()
            self.printOnConsole(oldPos, sender, color, piece, move.tag, promotedPiece)
            if self.colorTurn == "white":
                self.colorTurn = "black"
            elif self.colorTurn == "black":
                self.colorTurn = "white"
        elif self.buttonPressed == False:
            item = self.dataBoard.lookSpecificPosition(sender)
            if self.colorTurn != item.color:
                pb = self.buttons.get(sender)
                pb.setStatus(False)
                return False
            self.buttonPressed =  True
            self.selectedPiece = {"oldPos": sender, "color": item.color, "piece": item.piece}
            color = self.selectedPiece.get("color")
            piece = self.selectedPiece.get("piece")
            movements = self.dataBoard.checkValidMovements(sender, item.color, item.piece)
            try:
                if piece == "pawn":
                    for i in movements:
                        if i.tag == "promotion":
                            if color == "white":
                                cmb = self.cmb_white
                            elif color == "black":
                                cmb = self.cmb_black
                            cmb.setStyleSheet("background-color: rgb(0, 255, 0)")
                            QTimer.singleShot(200, lambda: cmb.setStyleSheet("background-color: rgb(51, 56, 68)"))
                        elif i.tag == "promotionAndCapture":
                            if color == "white":
                                cmb = self.cmb_white
                            elif color == "black":
                                cmb = self.cmb_black
                            cmb.setStyleSheet("background-color: rgb(0, 255, 0)")
                            QTimer.singleShot(200, lambda: cmb.setStyleSheet("background-color: rgb(51, 56, 68)"))
                        break
            except:
                pass
            self.validMovements(movements)
            self.disableEveryOtherButtons(sender)
        else:
            self.selectedPiece = {}
            self.buttonPressed = False
            self.enableAllButtons()
            self.resetMovements()

    def initializeGame(self):
        board = self.dataBoard.lookGameState()
        positions = list(board.keys())
        for pos in positions:
            item = board[pos]
            color = item.color
            piece = item.piece
            self.addPiece(pos, color, piece)

    def addPiece(self, pos, color, piece):
        validation = pos in  self.positionsBlack
        if validation == True:
            image = self.dico.get("normal").get("blackTile").get(color).get(piece)
            imageSelected = self.dico.get("selected").get("blackTile").get(color).get(piece)
        else:
            image = self.dico.get("normal").get("whiteTile").get(color).get(piece)
            imageSelected = self.dico.get("selected").get("whiteTile").get(color).get(piece)
        pb = self.buttons.get(pos)
        self.setIconsImage(pb, image, imageSelected)

    def validMovements(self, positions):
        for move in positions:
            pos = move.pos
            item = self.dataBoard.lookSpecificPosition(pos)
            if pos in  self.positionsBlack:
                image = self.dico.get("valid").get("blackTile").get(item.color).get(item.piece)
                imageSelected = self.dico.get("selected").get("blackTile").get(item.color).get(item.piece)
            elif pos in  self.positionsWhite:
                image = self.dico.get("valid").get("whiteTile").get(item.color).get(item.piece)
                imageSelected = self.dico.get("selected").get("whiteTile").get(item.color).get(item.piece)
            self.movements.append(pos)
            pb = self.buttons.get(pos)
            self.setIconsImage(pb, image, imageSelected)

    def resetMovements(self):
        for pos in self.movements:
            item = self.dataBoard.lookSpecificPosition(pos)
            if pos in self.positionsBlack:
                image = self.dico.get("normal").get("blackTile").get(item.color).get(item.piece)
                imageSelected = self.dico.get("selected").get("blackTile").get(item.color).get(item.piece)
            elif pos in  self.positionsWhite:
                image = self.dico.get("normal").get("whiteTile").get(item.color).get(item.piece)
                imageSelected = self.dico.get("selected").get("whiteTile").get(item.color).get(item.piece)
            pb = self.buttons.get(pos)
            self.setIconsImage(pb, image, imageSelected)
            self.movements = []

    def movePiece(self, oldPos, pos, color, piece):
        self.addPiece(oldPos, "empty", "empty")
        self.addPiece(pos, color, piece)

    def updateCMB(self):
        capturedWhite = self.dataBoard.capturedPieces["white"]
        capturedBlack = self.dataBoard.capturedPieces["black"]
        if capturedWhite != self.capturedPiecesWhite:
            newPiece = capturedWhite[-1]
            icon = QIcon(self.pieces["white"][newPiece])
            self.cmb_white.addItem(icon, newPiece)
            self.capturedPiecesWhite.append(newPiece)
        elif capturedBlack != self.capturedPiecesBlack:
            newPiece = capturedBlack[-1]
            icon = QIcon(self.pieces["black"][newPiece])
            self.cmb_black.addItem(icon, newPiece)
            self.capturedPiecesBlack.append(newPiece)

    def reupdateCMB(self, color):
        capturedWhite = self.dataBoard.capturedPieces["white"]
        capturedBlack = self.dataBoard.capturedPieces["black"]
        if color == "white":
            self.cmb_white.clear()
            self.capturedPiecesWhite = []
            for i in capturedWhite:
                icon = QIcon(self.pieces["white"][i])
                self.cmb_white.addItem(icon, i)
                self.capturedPiecesWhite.append(i)
        elif color == "black":
            self.cmb_black.clear()
            self.capturedPiecesBlack = []
            for i in capturedBlack:
                icon = QIcon(self.pieces["black"][i])
                self.cmb_black.addItem(icon, i)
                self.capturedPiecesBlack.append(i)

    def disableEveryOtherButtons(self, sender):
        for pos in self.positions:
            if pos == sender:
                pass
            elif pos in self.movements:
                pass
            else:
                pb = self.buttons.get(pos)
                pb.setEnabled(False)

    def enableAllButtons(self):
        for pos in self.positions:
            pb = self.buttons.get(pos)
            pb.setEnabled(True)

    def setIconsImage(self, pb, image, imageSelected):
        pb.setIcons(QPixmap(image).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
                                QPixmap(imageSelected).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def printOnConsole(self, oldPos, newPos, color, piece, tag, promotedPiece):
        if color == "white":
            otherColor = "black"
        elif color == "black":
            otherColor = "white"
        turn = self.dataBoard.currentTurn - 1
        if tag == "normal":
            text = f"[Turn {turn}] {color} {piece}: {oldPos} ⟶ {newPos}"
        elif tag == "capture":
            capturedPiece = self.dataBoard.capturedPieces[otherColor][-1]
            text = f"[Turn {turn}] {color} {piece}: {oldPos} ⟶ {newPos} (captured piece: {otherColor} {capturedPiece})"
        elif tag == "promotionAndCapture":
            capturedPiece = self.dataBoard.capturedPieces[otherColor][-1]
            text = f"[Turn {turn}] {color} {piece}: {oldPos} ⟶ {newPos} (promotion into {color} {promotedPiece})(captured piece: {otherColor} {capturedPiece})"
        elif tag == "promotion":
            text = f"[Turn {turn}] {color} {piece}: {oldPos} ⟶ {newPos} (promotion into {color} {promotedPiece})"
        elif tag == "bigCastling" or tag == "littleCastling":
            text = f"[Turn {turn}] {color} {tag}"
        elif tag == "passing":
            text = f"[Turn {turn}] {color} {piece}: {oldPos} ⟶ {newPos} (captured piece with passing: {otherColor} pawn)"
        else:
            text = f"[Turn {turn}] {color} {piece}: {oldPos} ⟶ {newPos} with the tag: {tag}"
        self.consoleView.showOnConsole(text)


    def createButtonsList(self):
        self.buttons["a8"] = self.pb_a8
        self.buttons["a7"] = self.pb_a7
        self.buttons["a6"] = self.pb_a6
        self.buttons["a5"] = self.pb_a5
        self.buttons["a4"] = self.pb_a4
        self.buttons["a3"] = self.pb_a3
        self.buttons["a2"] = self.pb_a2
        self.buttons["a1"] = self.pb_a1
        self.buttons["b8"] = self.pb_b8
        self.buttons["b7"] = self.pb_b7
        self.buttons["b6"] = self.pb_b6
        self.buttons["b5"] = self.pb_b5
        self.buttons["b4"] = self.pb_b4
        self.buttons["b3"] = self.pb_b3
        self.buttons["b2"] = self.pb_b2
        self.buttons["b1"] = self.pb_b1
        self.buttons["c8"] = self.pb_c8
        self.buttons["c7"] = self.pb_c7
        self.buttons["c6"] = self.pb_c6
        self.buttons["c5"] = self.pb_c5
        self.buttons["c4"] = self.pb_c4
        self.buttons["c3"] = self.pb_c3
        self.buttons["c2"] = self.pb_c2
        self.buttons["c1"] = self.pb_c1
        self.buttons["d8"] = self.pb_d8
        self.buttons["d7"] = self.pb_d7
        self.buttons["d6"] = self.pb_d6
        self.buttons["d5"] = self.pb_d5
        self.buttons["d4"] = self.pb_d4
        self.buttons["d3"] = self.pb_d3
        self.buttons["d2"] = self.pb_d2
        self.buttons["d1"] = self.pb_d1
        self.buttons["e8"] = self.pb_e8
        self.buttons["e7"] = self.pb_e7
        self.buttons["e6"] = self.pb_e6
        self.buttons["e5"] = self.pb_e5
        self.buttons["e4"] = self.pb_e4
        self.buttons["e3"] = self.pb_e3
        self.buttons["e2"] = self.pb_e2
        self.buttons["e1"] = self.pb_e1
        self.buttons["f8"] = self.pb_f8
        self.buttons["f7"] = self.pb_f7
        self.buttons["f6"] = self.pb_f6
        self.buttons["f5"] = self.pb_f5
        self.buttons["f4"] = self.pb_f4
        self.buttons["f3"] = self.pb_f3
        self.buttons["f2"] = self.pb_f2
        self.buttons["f1"] = self.pb_f1
        self.buttons["g8"] = self.pb_g8
        self.buttons["g7"] = self.pb_g7
        self.buttons["g6"] = self.pb_g6
        self.buttons["g5"] = self.pb_g5
        self.buttons["g4"] = self.pb_g4
        self.buttons["g3"] = self.pb_g3
        self.buttons["g2"] = self.pb_g2
        self.buttons["g1"] = self.pb_g1
        self.buttons["h8"] = self.pb_h8
        self.buttons["h7"] = self.pb_h7
        self.buttons["h6"] = self.pb_h6
        self.buttons["h5"] = self.pb_h5
        self.buttons["h4"] = self.pb_h4
        self.buttons["h3"] = self.pb_h3
        self.buttons["h2"] = self.pb_h2
        self.buttons["h1"] = self.pb_h1
