from typing import NamedTuple

class Infos(NamedTuple):
    dico: dict = None
    positionsBlack: list = None
    positionsWhite: list = None
    positions: list = None

class DictionaryAndList:
    def __init__(self):
        self.dico = {"normal" : {"blackTile":{"black":{}, "white":{}, "empty":{}}, "whiteTile":{"black":{}, "white":{}, "empty":{}}}, "selected": {"blackTile":{"black":{}, "white":{}, "empty":{}}, "whiteTile":{"black":{}, "white":{}, "empty":{}}}, "valid": {"blackTile":{"black":{}, "white":{}, "empty":{}}, "whiteTile":{"black":{}, "white":{}, "empty":{}}}}
        self.createDico()
        self.positionsBlack = []
        self.positionsWhite = []
        self.createPositions()
        self.positions = self.positionsWhite + self.positionsBlack

    def returnInfos(self):
        return Infos(self.dico, self.positionsBlack, self.positionsWhite, self.positions)

    def createPositions(self):
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

    def createDico(self):
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