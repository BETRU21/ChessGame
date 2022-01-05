from typing import NamedTuple

class Turn(NamedTuple):
    oldPos: str = None
    newPos: str = None
    color: str = None
    piece: str = None



class DataBoard:
	def __init__(self):
		self.validLetters = ["a","b","c","d","e","f","g","h"]
		self.validNumbers = [8,7,6,5,4,3,2,1]
		self.gameState = {}
		self.capturedPieces = {"white": [], "black": []}
		self.initializeGameState()
		self.actualTurn = 1
		self.log = []

	def lookSpecificTurn(self, turn):
		if turn <= 0:
			raise ValueError("Turn must be greater or equal to 1")
		index = turn - 1
		return self.log[index]

	def addInLog(self, oldPos, newPos, color, piece):
		turn = Turn(oldPos, newPos, color, piece)
		self.log.append(turn)

	def promotionInCapturedPieces(self, color, promotedPiece, newPiece):
		index = self.capturedPieces[color].index(promotedPiece)
		self.capturedPieces[color][index] = newPiece

	def lookGameState(self):
		return self.gameState

	def lookSpecificPosition(self, pos):
		return self.gameState.get(pos)

	def checkValidMovements(self, pos, color, piece):
		if piece == "king":
			validMovements = self.kingMovements(pos, color)
		elif piece == "queen":
			validMovements = self.queenMovements(pos, color)
		elif piece == "rook":
			validMovements = self.rookMovements(pos, color)
		elif piece == "knight":
			validMovements = self.knightMovements(pos, color)
		elif piece == "bishop":
			validMovements = self.bishopMovements(pos, color)
		elif piece == "pawn":
			validMovements = self.pawnMovements(pos, color)
		elif piece == "empty":
			validMovements = []
		else:
			validMovements = []
			print("Invalid movements")
		return validMovements

	def addItemInGameState(self, pos, item):
		self.gameState[pos] = item
	
	def moveItemInGameState(self, oldPos, newPos, color, piece, promotePiece="empty"):
		passing = False
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		item = self.gameState[oldPos]
		if item[0] != color:
			raise ValueError("Color don't match")
		elif item[1] != piece:
			raise ValueError("Piece don't match")
		else:
			if piece == "king":
				validMovements = self.kingMovements(oldPos, color)
			elif piece == "queen":
				validMovements = self.queenMovements(oldPos, color)
			elif piece == "rook":
				validMovements = self.rookMovements(oldPos, color)
			elif piece == "knight":
				validMovements = self.knightMovements(oldPos, color)
			elif piece == "bishop":
				validMovements = self.bishopMovements(oldPos, color)
			elif piece == "pawn":
				validMovements = self.pawnMovements(oldPos, color)
				if "promotion" in validMovements:
					if promotePiece in self.capturedPieces[color]:
						item = (item[0], promotePiece)
						self.promotionInCapturedPieces(color, promotePiece, piece)
				if "passing" in validMovements:
					if newPos == validMovements[0]:
						if color == "white":
							capturePos = newPos[0] + "5"
						if color == "black":
							capturePos = newPos[0] + "4"
						passing = capturePos
						itemAtCapturePos = self.gameState[capturePos]
						self.capturedPieces[itemAtCapturePos[0]].append(itemAtCapturePos[1])
						self.addItemInGameState(capturePos, ("empty", "empty"))

			validation = newPos in  validMovements
			if validation == False:
				raise RuntimeError("This movement is invalid")
			itemAtNewPos = self.gameState[newPos]
			if itemAtNewPos == ("empty", "empty"):
				pass
			else:
				self.capturedPieces[itemAtNewPos[0]].append(itemAtNewPos[1])
			self.addItemInGameState(oldPos, ("empty", "empty"))
			self.addItemInGameState(newPos, item)
			self.addInLog(oldPos, newPos, color, piece)
			self.actualTurn += 1
			return passing

	# Non-Public Functions

	def initializeGameState(self):
		for i in self.validLetters:
			for j in self.validNumbers:
				self.gameState[f"{i}{j}"] = ("empty", "empty")
		for i in ["a7","b7","c7","d7","e7","f7","g7","h7"]:
			self.addItemInGameState(i, ("black", "pawn"))
		self.addItemInGameState("a8", ("black", "rook"))
		self.addItemInGameState("h8", ("black", "rook"))
		self.addItemInGameState("b8", ("black", "knight"))
		self.addItemInGameState("g8", ("black", "knight"))
		self.addItemInGameState("c8", ("black", "bishop"))
		self.addItemInGameState("f8", ("black", "bishop"))
		self.addItemInGameState("d8", ("black", "queen"))
		self.addItemInGameState("e8", ("black", "king"))
		for i in ["a2","b2","c2","d2","e2","f2","g2","h2"]:
			self.addItemInGameState(i, ("white", "pawn"))
		self.addItemInGameState("a1", ("white", "rook"))
		self.addItemInGameState("h1", ("white", "rook"))
		self.addItemInGameState("b1", ("white", "knight"))
		self.addItemInGameState("g1", ("white", "knight"))
		self.addItemInGameState("c1", ("white", "bishop"))
		self.addItemInGameState("f1", ("white", "bishop"))
		self.addItemInGameState("d1", ("white", "queen"))
		self.addItemInGameState("e1", ("white", "king"))

	def translatePositionToTuple(self, pos):
		dico = {"a": 8, "b": 7, "c": 6, "d": 5, "e": 4, "f": 3, "g": 2, "h": 1}
		line = int(pos[1])
		index = dico[pos[0]]
		return (index, line)

	def translateTupleToPosition(self, pos):
		dico = {"8": "a", "7": "b", "6": "c", "5": "d", "4": "e", "3": "f", "2": "g", "1": "h"}
		line = f"{pos[1]}"
		index = dico[f"{pos[0]}"]
		return f"{index}{line}"
	
	def positionTupleFilter(self, pos):
		if pos[0] < 1:
			raise ValueError("InvalidPosition")
		elif pos[0] > 8:
			raise ValueError("InvalidPosition")
		elif pos[1] < 1:
			raise ValueError("InvalidPosition")
		elif pos[1] > 8:
			raise ValueError("InvalidPosition")
		else:
			return self.translateTupleToPosition(pos)

	# Pieces Movements

	def kingMovements(self, pos, color):
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		pos = self.translatePositionToTuple(pos)
		PossibleMovements = []
		PossibleMovements.append((pos[0]+1,pos[1]))
		PossibleMovements.append((pos[0]+1,pos[1]+1))
		PossibleMovements.append((pos[0]+1,pos[1]-1))
		PossibleMovements.append((pos[0]-1,pos[1]))
		PossibleMovements.append((pos[0]-1,pos[1]+1))
		PossibleMovements.append((pos[0]-1,pos[1]-1))
		PossibleMovements.append((pos[0],pos[1]+1))
		PossibleMovements.append((pos[0],pos[1]-1))
		realMovements = []
		for i in PossibleMovements:
			try:
				pos = self.positionTupleFilter(i)
				realMovements.append(pos)
			except:
				pass
		validMovements = []
		for i in realMovements:
			item = self.lookSpecificPosition(i)
			if item[0] == color:
				pass
			else:
				validMovements.append(i)
		return validMovements

	def knightMovements(self, pos, color):
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		pos = self.translatePositionToTuple(pos)
		PossibleMovements = []
		PossibleMovements.append((pos[0]+2,pos[1]-1))
		PossibleMovements.append((pos[0]+2,pos[1]+1))
		PossibleMovements.append((pos[0]-2,pos[1]-1))
		PossibleMovements.append((pos[0]-2,pos[1]+1))
		PossibleMovements.append((pos[0]+1,pos[1]+2))
		PossibleMovements.append((pos[0]-1,pos[1]+2))
		PossibleMovements.append((pos[0]+1,pos[1]-2))
		PossibleMovements.append((pos[0]-1,pos[1]-2))
		realMovements = []
		for i in PossibleMovements:
			try:
				pos = self.positionTupleFilter(i)
				realMovements.append(pos)
			except:
				pass
		validMovements = []
		for i in realMovements:
			item = self.lookSpecificPosition(i)
			if item[0] == color:
				pass
			else:
				validMovements.append(i)
		return validMovements

	def rookMovements(self, pos, color):
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		posT = self.translatePositionToTuple(pos)
		validMovements = []
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1])
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1])
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]+i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]-i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		return validMovements

	def bishopMovements(self, pos, color):
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		posT = self.translatePositionToTuple(pos)
		validMovements = []
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]+i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]-i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]+i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]-i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		return validMovements

	def queenMovements(self, pos, color):
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		posT = self.translatePositionToTuple(pos)
		validMovements = []
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1])
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1])
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]+i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]-i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]+i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]-i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]+i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]-i)
			try:
				pos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == False:
						validMovements.append(pos)
			except:
				pass
		return validMovements

	def pawnMovements(self, pos, color):
		passing = False
		promotion = False
		posT = self.translatePositionToTuple(pos)
		validMovements = []
		if color == "white":
			otherColor = "black"
			try:
				if pos in ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"]:
					newPos1 = (posT[0]-1, posT[1])
					pos1 = self.positionTupleFilter(newPos1)
					item1 = self.lookSpecificPosition(pos1)
					if item1 == ("black", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == pos1[0] + "7":
							if lastTurn.newPos == pos1[0] + "5":
								validMovements.append(pos1[0] + "6" )
								passing = True

					newPos2 = (posT[0]+1, posT[1])
					pos2 = self.positionTupleFilter(newPos2)
					item2 = self.lookSpecificPosition(pos2)
					if item2 == ("black", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == pos2[0] + "7":
							if lastTurn.newPos == pos2[0] + "5":
								validMovements.append(pos2[0] + "6")
								passing = True
			except:
				pass
			newPos = (posT[0], posT[1]+1)
			try:
				pos = self.positionTupleFilter(newPos)
				if pos in ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
					promotion = True
				item = self.lookSpecificPosition(pos)
				if item[0] == "empty":
					validMovements.append(pos)
					if posT[1] == 2:
						newPos = (posT[0], posT[1]+2)
						try:
							pos = self.positionTupleFilter(newPos)
							item = self.lookSpecificPosition(pos)
							if item[0] == "empty":
								validMovements.append(pos)
						except:
							pass
			except:
				pass
			newPos = (posT[0]+1, posT[1]+1)
			try:
				pos = self.positionTupleFilter(newPos)
				if pos in ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
					promotion = True
				item = self.lookSpecificPosition(pos)
				if item[0] == otherColor:
					validMovements.append(pos)
			except:
				pass
			newPos = (posT[0]-1, posT[1]+1)
			try:
				pos = self.positionTupleFilter(newPos)
				if pos in ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
					promotion = True
				item = self.lookSpecificPosition(pos)
				if item[0] == otherColor:
					validMovements.append(pos)
			except:
				pass
			if promotion == True:
				validMovements.append("promotion")
			if passing == True:
				validMovements.append("passing")
			return validMovements


		elif color == "black":
			otherColor = "white"
			try:
				if pos in ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"]:
					newPos1 = (posT[0]-1, posT[1])
					pos1 = self.positionTupleFilter(newPos1)
					item1 = self.lookSpecificPosition(pos1)
					if item1 == ("white", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == pos1[0] + "2":
							if lastTurn.newPos == pos1[0] + "4":
								validMovements.append(pos1[0] + "3" )
								passing = True

					newPos2 = (posT[0]+1, posT[1])
					pos2 = self.positionTupleFilter(newPos2)
					item2 = self.lookSpecificPosition(pos2)
					if item2 == ("white", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == pos2[0] + "2":
							if lastTurn.newPos == pos2[0] + "4":
								validMovements.append(pos2[0] + "3")
								passing = True
			except:
				pass
			newPos = (posT[0], posT[1]-1)
			try:
				pos = self.positionTupleFilter(newPos)
				if pos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
					promotion = True
				item = self.lookSpecificPosition(pos)
				if item[0] == "empty":
					validMovements.append(pos)
					if posT[1] == 7:
						newPos = (posT[0], posT[1]-2)
						try:
							pos = self.positionTupleFilter(newPos)
							item = self.lookSpecificPosition(pos)
							if item[0] == "empty":
								validMovements.append(pos)
						except:
							pass
			except:
				pass
			newPos = (posT[0]+1, posT[1]-1)
			try:
				pos = self.positionTupleFilter(newPos)
				if pos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
					promotion = True
				item = self.lookSpecificPosition(pos)
				if item[0] == otherColor:
					validMovements.append(pos)
			except:
				pass
			newPos = (posT[0]-1, posT[1]-1)
			try:
				pos = self.positionTupleFilter(newPos)
				if pos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
					promotion = True
				item = self.lookSpecificPosition(pos)
				if item[0] == otherColor:
					validMovements.append(pos)
			except:
				pass
			if promotion == True:
				validMovements.append("promotion")
			if passing == True:
				validMovements.append("passing")
			return validMovements
		else:
			raise ValueError("Color is invalid")


dataBoard = DataBoard()
dataBoard.moveItemInGameState("d2", "d4", "white", "pawn")
dataBoard.moveItemInGameState("d4", "d5", "white", "pawn")
dataBoard.moveItemInGameState("e7", "e5", "black", "pawn")
#dataBoard.moveItemInGameState("c7", "c5", "black", "pawn")
dataBoard.pawnMovements("d5", "white")

# dataBoard.moveItemInGameState("d7", "d5", "black", "pawn")
# dataBoard.moveItemInGameState("d5", "d4", "black", "pawn")
# dataBoard.moveItemInGameState("c2", "c4", "white", "pawn")
# dataBoard.moveItemInGameState("e2", "e4", "white", "pawn")
# dataBoard.pawnMovements("d4", "black")
# oldPos, sender, color, piece, promotedPiece