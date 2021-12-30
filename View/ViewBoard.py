from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt
from PyQt5.Qt import QPixmap
from PyQt5 import uic
from PyQt5 import QtGui
import os

MainWindowPath = os.path.dirname(os.path.realpath(__file__)) + '/ui{}BoardWindow.ui'.format(os.sep)
Ui_MainWindow, QtBaseClass = uic.loadUiType(MainWindowPath)

class ViewBoard(QWidget, Ui_MainWindow):
    def __init__(self, dataBoard=None):
        super(ViewBoard, self).__init__()
        self.setupUi(self)
        self.dico = {"normal" : {"blackTile":{"black":{}, "white":{}, "empty":{}}, "whiteTile":{"black":{}, "white":{}, "empty":{}}}, "selected": {"blackTile":{"black":{}, "white":{}, "empty":{}}, "whiteTile":{"black":{}, "white":{}, "empty":{}}}, "valid": {"blackTile":{"black":{}, "white":{}, "empty":{}}, "whiteTile":{"black":{}, "white":{}, "empty":{}}}}
        self.buildDico()
        self.movements = []
        self.selectedPiece = ()
        self.dataBoard = dataBoard 
        self.buttonPressed = False
        self.positionsBlack = []
        self.positionsWhite = []
        self.buildPositions()
        self.positions = self.positionsWhite + self.positionsBlack
        self.buttons = {}
        self.buildButtonsList()
        self.connectWidgets()
        self.initializeGame()

    def initializeGame(self):
        board = self.dataBoard.lookGameState()
        positions = list(board.keys())
        for i in positions:
            info = board[i]
            color = info[0]
            piece = info[1]
            self.addPiece(i, color, piece)

    def addPiece(self, pos, color, piece):
        validation = pos in  self.positionsBlack
        if validation == True:
            image = self.dico.get("normal").get("blackTile").get(color).get(piece)
            imageSelected = self.dico.get("selected").get("blackTile").get(color).get(piece)
        else:
            image = self.dico.get("normal").get("whiteTile").get(color).get(piece)
            imageSelected = self.dico.get("selected").get("whiteTile").get(color).get(piece)
        pb = self.buttons.get(pos)
        pb.setIcons(QPixmap(image).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
                                QPixmap(imageSelected).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    def validMovements(self, positions):
        for i in positions:
            info = self.dataBoard.lookSpecificPosition(i)
            color = info[0]
            piece = info[1]
            validation = i in  self.positionsBlack
            if validation == True:
                image = self.dico.get("valid").get("blackTile").get(color).get(piece)
                imageSelected = self.dico.get("selected").get("blackTile").get(color).get(piece)
            else:
                image = self.dico.get("valid").get("whiteTile").get(color).get(piece)
                imageSelected = self.dico.get("selected").get("whiteTile").get(color).get(piece)
            self.movements.append(i)
            pb = self.buttons.get(i)
            pb.setIcons(QPixmap(image).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
                                QPixmap(imageSelected).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))


    def resetMovements(self):
        for i in self.movements:
            info = self.dataBoard.lookSpecificPosition(i)
            color = info[0]
            piece = info[1]
            validation = i in  self.positionsBlack
            if validation == True:
                image = self.dico.get("normal").get("blackTile").get(color).get(piece)
                imageSelected = self.dico.get("selected").get("blackTile").get(color).get(piece)
            else:
                image = self.dico.get("normal").get("whiteTile").get(color).get(piece)
                imageSelected = self.dico.get("selected").get("whiteTile").get(color).get(piece)
            pb = self.buttons.get(i)
            pb.setIcons(QPixmap(image).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation),
                                QPixmap(imageSelected).scaled(50, 50, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.movements = []

    def movePiece(self, oldPos, pos, color, piece):
        self.addPiece(oldPos, "empty", "empty")
        self.addPiece(pos, color, piece)

    def connectWidgets(self):
        for i in self.positions:
            pb = self.buttons.get(i)
            pb.clicked.connect(self.buttonAction)

    def buttonAction(self):
        sender = self.sender().text()
        if sender in self.movements:
            oldPos = self.selectedPiece.get("oldPos")
            color = self.selectedPiece.get("color")
            piece = self.selectedPiece.get("piece")
            self.dataBoard.moveItemInGameState(oldPos, sender, color, piece)
            self.movePiece(oldPos, sender, color, piece)
            self.selectedPiece = {}
            self.buttonPressed = False
            self.enableAllButtons()
            self.resetMovements()
            oldPb = self.buttons.get(oldPos)
            oldPb.setStatus(False)
            pb = self.buttons.get(sender)
            pb.setStatus(False)

        elif self.buttonPressed == False:
            self.buttonPressed =  True
            info = self.dataBoard.lookSpecificPosition(sender)
            self.selectedPiece = {"oldPos": sender, "color": info[0], "piece": info[1]}
            movements = self.dataBoard.checkValidMovements(sender, info[0], info[1])
            self.validMovements(movements)
            self.disableEveryOtherButtons(sender)
        else:
            self.selectedPiece = {}
            self.buttonPressed = False
            self.enableAllButtons()
            self.resetMovements()

    def disableEveryOtherButtons(self, sender):
        for i in self.positions:
            if i == sender:
                pass
            elif i in self.movements:
                pass
            else:
                pb = self.buttons.get(i)
                pb.setEnabled(False)

    def enableAllButtons(self):
        for i in self.positions:
            pb = self.buttons.get(i)
            pb.setEnabled(True)

    def buildPositions(self):
        letters = ["a", "c", "e", "g"]
        numbers = ["7", "5", "3", "1"]
        for i in letters:
            for j in numbers:
                self.positionsBlack.append(i + j)
        letters = ["b", "d", "f", "h"]
        numbers = ["8", "6", "4", "2"]
        for i in letters:
            for j in numbers:
                self.positionsBlack.append(i + j)
        letters = ["a", "c", "e", "g"]
        numbers = ["8", "6", "4", "2"]
        for i in letters:
            for j in numbers:
                self.positionsWhite.append(i + j)
        letters = ["b", "d", "f", "h"]
        numbers = ["7", "5", "3", "1"]
        for i in letters:
            for j in numbers:
                self.positionsWhite.append(i + j)

    def buildButtonsList(self):
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

    def buildDico(self):
        self.dico["normal"]["blackTile"]["empty"]["empty"] = "./View/icons/black_tile_empty.png"
        self.dico["normal"]["blackTile"]["black"]["king"] = "./View/icons/black_tile_blackKing.png"
        self.dico["normal"]["blackTile"]["black"]["queen"] = "./View/icons/black_tile_blackQueen.png"
        self.dico["normal"]["blackTile"]["black"]["rook"] = "./View/icons/black_tile_blackRook.png"
        self.dico["normal"]["blackTile"]["black"]["bishop"] = "./View/icons/black_tile_blackBishop.png"
        self.dico["normal"]["blackTile"]["black"]["knight"] = "./View/icons/black_tile_blackKnight.png"
        self.dico["normal"]["blackTile"]["black"]["pawn"] = "./View/icons/black_tile_blackPawn.png"
        self.dico["normal"]["blackTile"]["white"]["king"] = "./View/icons/black_tile_whiteKing.png"
        self.dico["normal"]["blackTile"]["white"]["queen"] = "./View/icons/black_tile_whiteQueen.png"
        self.dico["normal"]["blackTile"]["white"]["rook"] = "./View/icons/black_tile_whiteRook.png"
        self.dico["normal"]["blackTile"]["white"]["bishop"] = "./View/icons/black_tile_whiteBishop.png"
        self.dico["normal"]["blackTile"]["white"]["knight"] = "./View/icons/black_tile_whiteKnight.png"
        self.dico["normal"]["blackTile"]["white"]["pawn"] = "./View/icons/black_tile_whitePawn.png"
        self.dico["normal"]["whiteTile"]["empty"]["empty"] = "./View/icons/white_tile_empty.png"
        self.dico["normal"]["whiteTile"]["black"]["king"] = "./View/icons/white_tile_blackKing.png"
        self.dico["normal"]["whiteTile"]["black"]["queen"] = "./View/icons/white_tile_blackQueen.png"
        self.dico["normal"]["whiteTile"]["black"]["rook"] = "./View/icons/white_tile_blackRook.png"
        self.dico["normal"]["whiteTile"]["black"]["bishop"] = "./View/icons/white_tile_blackBishop.png"
        self.dico["normal"]["whiteTile"]["black"]["knight"] = "./View/icons/white_tile_blackKnight.png"
        self.dico["normal"]["whiteTile"]["black"]["pawn"] = "./View/icons/white_tile_blackPawn.png"
        self.dico["normal"]["whiteTile"]["white"]["king"] = "./View/icons/white_tile_whiteKing.png"
        self.dico["normal"]["whiteTile"]["white"]["queen"] = "./View/icons/white_tile_whiteQueen.png"
        self.dico["normal"]["whiteTile"]["white"]["rook"] = "./View/icons/white_tile_whiteRook.png"
        self.dico["normal"]["whiteTile"]["white"]["bishop"] = "./View/icons/white_tile_whiteBishop.png"
        self.dico["normal"]["whiteTile"]["white"]["knight"] = "./View/icons/white_tile_whiteKnight.png"
        self.dico["normal"]["whiteTile"]["white"]["pawn"] = "./View/icons/white_tile_whitePawn.png"

        self.dico["selected"]["blackTile"]["empty"]["empty"] = "./View/icons/black_tile_selected_empty.png"
        self.dico["selected"]["blackTile"]["black"]["king"] = "./View/icons/black_tile_selected_blackKing.png"
        self.dico["selected"]["blackTile"]["black"]["queen"] = "./View/icons/black_tile_selected_blackQueen.png"
        self.dico["selected"]["blackTile"]["black"]["rook"] = "./View/icons/black_tile_selected_blackRook.png"
        self.dico["selected"]["blackTile"]["black"]["bishop"] = "./View/icons/black_tile_selected_blackBishop.png"
        self.dico["selected"]["blackTile"]["black"]["knight"] = "./View/icons/black_tile_selected_blackKnight.png"
        self.dico["selected"]["blackTile"]["black"]["pawn"] = "./View/icons/black_tile_selected_blackPawn.png"
        self.dico["selected"]["blackTile"]["white"]["king"] = "./View/icons/black_tile_selected_whiteKing.png"
        self.dico["selected"]["blackTile"]["white"]["queen"] = "./View/icons/black_tile_selected_whiteQueen.png"
        self.dico["selected"]["blackTile"]["white"]["rook"] = "./View/icons/black_tile_selected_whiteRook.png"
        self.dico["selected"]["blackTile"]["white"]["bishop"] = "./View/icons/black_tile_selected_whiteBishop.png"
        self.dico["selected"]["blackTile"]["white"]["knight"] = "./View/icons/black_tile_selected_whiteKnight.png"
        self.dico["selected"]["blackTile"]["white"]["pawn"] = "./View/icons/black_tile_selected_whitePawn.png"
        self.dico["selected"]["whiteTile"]["empty"]["empty"] = "./View/icons/white_tile_selected_empty.png"
        self.dico["selected"]["whiteTile"]["black"]["king"] = "./View/icons/white_tile_selected_blackKing.png"
        self.dico["selected"]["whiteTile"]["black"]["queen"] = "./View/icons/white_tile_selected_blackQueen.png"
        self.dico["selected"]["whiteTile"]["black"]["rook"] = "./View/icons/white_tile_selected_blackRook.png"
        self.dico["selected"]["whiteTile"]["black"]["bishop"] = "./View/icons/white_tile_selected_blackBishop.png"
        self.dico["selected"]["whiteTile"]["black"]["knight"] = "./View/icons/white_tile_selected_blackKnight.png"
        self.dico["selected"]["whiteTile"]["black"]["pawn"] = "./View/icons/white_tile_selected_blackPawn.png"
        self.dico["selected"]["whiteTile"]["white"]["king"] = "./View/icons/white_tile_selected_whiteKing.png"
        self.dico["selected"]["whiteTile"]["white"]["queen"] = "./View/icons/white_tile_selected_whiteQueen.png"
        self.dico["selected"]["whiteTile"]["white"]["rook"] = "./View/icons/white_tile_selected_whiteRook.png"
        self.dico["selected"]["whiteTile"]["white"]["bishop"] = "./View/icons/white_tile_selected_whiteBishop.png"
        self.dico["selected"]["whiteTile"]["white"]["knight"] = "./View/icons/white_tile_selected_whiteKnight.png"
        self.dico["selected"]["whiteTile"]["white"]["pawn"] = "./View/icons/white_tile_selected_whitePawn.png"

        self.dico["valid"]["blackTile"]["empty"]["empty"] = "./View/icons/black_tile_valid_empty.png"
        self.dico["valid"]["blackTile"]["black"]["king"] = "./View/icons/black_tile_valid_blackKing.png"
        self.dico["valid"]["blackTile"]["black"]["queen"] = "./View/icons/black_tile_valid_blackQueen.png"
        self.dico["valid"]["blackTile"]["black"]["rook"] = "./View/icons/black_tile_valid_blackRook.png"
        self.dico["valid"]["blackTile"]["black"]["bishop"] = "./View/icons/black_tile_valid_blackBishop.png"
        self.dico["valid"]["blackTile"]["black"]["knight"] = "./View/icons/black_tile_valid_blackKnight.png"
        self.dico["valid"]["blackTile"]["black"]["pawn"] = "./View/icons/black_tile_valid_blackPawn.png"
        self.dico["valid"]["blackTile"]["white"]["king"] = "./View/icons/black_tile_valid_whiteKing.png"
        self.dico["valid"]["blackTile"]["white"]["queen"] = "./View/icons/black_tile_valid_whiteQueen.png"
        self.dico["valid"]["blackTile"]["white"]["rook"] = "./View/icons/black_tile_valid_whiteRook.png"
        self.dico["valid"]["blackTile"]["white"]["bishop"] = "./View/icons/black_tile_valid_whiteBishop.png"
        self.dico["valid"]["blackTile"]["white"]["knight"] = "./View/icons/black_tile_valid_whiteKnight.png"
        self.dico["valid"]["blackTile"]["white"]["pawn"] = "./View/icons/black_tile_valid_whitePawn.png"
        self.dico["valid"]["whiteTile"]["empty"]["empty"] = "./View/icons/white_tile_valid_empty.png"
        self.dico["valid"]["whiteTile"]["black"]["king"] = "./View/icons/white_tile_valid_blackKing.png"
        self.dico["valid"]["whiteTile"]["black"]["queen"] = "./View/icons/white_tile_valid_blackQueen.png"
        self.dico["valid"]["whiteTile"]["black"]["rook"] = "./View/icons/white_tile_valid_blackRook.png"
        self.dico["valid"]["whiteTile"]["black"]["bishop"] = "./View/icons/white_tile_valid_blackBishop.png"
        self.dico["valid"]["whiteTile"]["black"]["knight"] = "./View/icons/white_tile_valid_blackKnight.png"
        self.dico["valid"]["whiteTile"]["black"]["pawn"] = "./View/icons/white_tile_valid_blackPawn.png"
        self.dico["valid"]["whiteTile"]["white"]["king"] = "./View/icons/white_tile_valid_whiteKing.png"
        self.dico["valid"]["whiteTile"]["white"]["queen"] = "./View/icons/white_tile_valid_whiteQueen.png"
        self.dico["valid"]["whiteTile"]["white"]["rook"] = "./View/icons/white_tile_valid_whiteRook.png"
        self.dico["valid"]["whiteTile"]["white"]["bishop"] = "./View/icons/white_tile_valid_whiteBishop.png"
        self.dico["valid"]["whiteTile"]["white"]["knight"] = "./View/icons/white_tile_valid_whiteKnight.png"
        self.dico["valid"]["whiteTile"]["white"]["pawn"] = "./View/icons/white_tile_valid_whitePawn.png"