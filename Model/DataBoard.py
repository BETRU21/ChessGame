from typing import NamedTuple

class Turn(NamedTuple):
    oldPos: str = None
    newPos: str = None
    color: str = None
    piece: str = None

class Movement(NamedTuple):
	pos: str = None
	tag: str = None


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
		if color == "white":
			if self.actualTurn%2 == 0:
				raise RuntimeError("This is not your turn")
			otherColor = "black"
		elif color == "black":
			if self.actualTurn%2 == 1:
				raise RuntimeError("This is not your turn")
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

			validMove = False
			for i in validMovements:
				if i.pos == newPos:
					validMove = i
			if validMove == False:
				raise RuntimeError("This movement is invalid")

			if validMove.tag == "promotion":
					if promotePiece in self.capturedPieces[color]:
						item = (item[0], promotePiece)
						self.promotionInCapturedPieces(color, promotePiece, piece)

			if validMove.tag == "passing":
				if color == "white":
					capturePos = newPos[0] + "5"
				if color == "black":
					capturePos = newPos[0] + "4"
				itemAtCapturePos = self.gameState[capturePos]
				self.capturedPieces[itemAtCapturePos[0]].append(itemAtCapturePos[1])
				self.addItemInGameState(capturePos, ("empty", "empty"))

			if validMove.tag == "littleCastling":
				if color == "white":
					self.addItemInGameState("h1", ("empty", "empty"))
					self.addItemInGameState("f1", ("white", "rook"))
				if color == "black":
					self.addItemInGameState("h8", ("empty", "empty"))
					self.addItemInGameState("f8", ("black", "rook"))

			if validMove.tag == "bigCastling":
				if color == "white":
					self.addItemInGameState("a1", ("empty", "empty"))
					self.addItemInGameState("d1", ("white", "rook"))
				if color == "black":
					self.addItemInGameState("a8", ("empty", "empty"))
					self.addItemInGameState("d8", ("black", "rook"))

			itemAtNewPos = self.gameState[newPos]
			if itemAtNewPos == ("empty", "empty"):
				pass
			else:
				self.capturedPieces[itemAtNewPos[0]].append(itemAtNewPos[1])
			self.addItemInGameState(oldPos, ("empty", "empty"))
			self.addItemInGameState(newPos, item)
			self.addInLog(oldPos, newPos, color, piece)
			self.actualTurn += 1
			return validMove

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
		validBigCastling = True
		validLittleCastling = True
		if color == "white":
			otherColor = "black"
		elif color == "black":
			otherColor = "white"
		else:
			raise ValueError("Color is invalid")
		posT = self.translatePositionToTuple(pos)
		PossibleMovements = []
		PossibleMovements.append((posT[0]+1,posT[1]))
		PossibleMovements.append((posT[0]+1,posT[1]+1))
		PossibleMovements.append((posT[0]+1,posT[1]-1))
		PossibleMovements.append((posT[0]-1,posT[1]))
		PossibleMovements.append((posT[0]-1,posT[1]+1))
		PossibleMovements.append((posT[0]-1,posT[1]-1))
		PossibleMovements.append((posT[0],posT[1]+1))
		PossibleMovements.append((posT[0],posT[1]-1))
		realMovements = []
		for i in PossibleMovements:
			try:
				position = self.positionTupleFilter(i)
				realMovements.append(position)
			except:
				pass
		validMovements = []
		for i in realMovements:
			item = self.lookSpecificPosition(i)
			if item[0] == color:
				pass
			elif item[0] == otherColor:
				move = Movement(i, "capture")
				validMovements.append(move)
			else:
				move = Movement(i, "normal")
				validMovements.append(move)
		####
		if color == "black":
			if pos == "e8":
				try:
					for i in self.log:
						if i.piece == "king":
							if i.color == "black":
								validBigCastling = False
								validLittleCastling = False
								break
						if i.piece == "rook":
							if i.color == "black":
								if i.oldPos == "a8":
									validBigCastling = False
								if i.oldPos == "g8":
									validLittleCastling = False

				except:
					pass

				if self.lookSpecificPosition("f8") == ("empty", "empty"):
					if self.lookSpecificPosition("g8") == ("empty", "empty"):
						if validLittleCastling == True:
							move = Movement("g8", "littleCastling")
							validMovements.append(move)

				if self.lookSpecificPosition("d8") == ("empty", "empty"):
					if self.lookSpecificPosition("c8") == ("empty", "empty"):
						if self.lookSpecificPosition("b8") == ("empty", "empty"):
							if validBigCastling == True:
								move = Movement("c8", "bigCastling")
								validMovements.append(move)

		if color == "white":
			if pos == "e1":
				try:
					for i in self.log:
						if i.piece == "king":
							if i.color == "white":
								validBigCastling = False
								validLittleCastling = False
								break
						if i.piece == "rook":
							if i.color == "white":
								if i.oldPos == "a1":
									validBigCastling = False
								if i.oldPos == "g1":
									validLittleCastling = False

				except:
					pass

				if self.lookSpecificPosition("f1") == ("empty", "empty"):
					if self.lookSpecificPosition("g1") == ("empty", "empty"):
						if validLittleCastling == True:
							move = Movement("g1", "littleCastling")
							validMovements.append(move)

				if self.lookSpecificPosition("f1") == ("empty", "empty"):
					if self.lookSpecificPosition("c1") == ("empty", "empty"):
						if self.lookSpecificPosition("b1") == ("empty", "empty"):
							if validBigCastling == True:
								move = Movement("c1", "bigCastling")
								validMovements.append(move)

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
			elif item[0] == otherColor:
				move = Movement(i, "capture")
				validMovements.append(move)
			else:
				move = Movement(i, "normal")
				validMovements.append(move)
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
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1])
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]+i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]-i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
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
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]-i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]+i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]-i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
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
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1])
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == True:
						pass
					else:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]+i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0],posT[1]-i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]+i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]+i,posT[1]-i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]+i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		reachMax = False
		for i in [1,2,3,4,5,6,7]:
			newPos = (posT[0]-i,posT[1]-i)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == color:
					reachMax = True
				elif item[0] == otherColor:
					if reachMax == False:
						reachMax = True
						move = Movement(newPos, "capture")
						validMovements.append(move)
				else:
					if reachMax == False:
						move = Movement(newPos, "normal")
						validMovements.append(move)
			except:
				pass
		return validMovements

	def pawnMovements(self, pos, color):
		posT = self.translatePositionToTuple(pos)
		validMovements = []
		if color == "white":
			otherColor = "black"
			try:
				if pos in ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"]:
					newPos = (posT[0]-1, posT[1])
					newPos = self.positionTupleFilter(newPos)
					item = self.lookSpecificPosition(newPos)
					if item == ("black", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == newPos[0] + "7":
							if lastTurn.newPos == newPos[0] + "5":
								newPos = newPos[0] + "6"
								move = Movement(newPos, "passing")
								validMovements.append(move)

					newPos = (posT[0]+1, posT[1])
					newPos = self.positionTupleFilter(newPos)
					item = self.lookSpecificPosition(newPos)
					if item == ("black", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == newPos[0] + "7":
							if lastTurn.newPos == newPos[0] + "5":
								newPos = newPos[0] + "6"
								move = Movement(newPos, "passing")
								validMovements.append(move)
			except:
				pass
			newPos = (posT[0], posT[1]+1)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == "empty":
					if newPos in ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
						move = Movement(newPos, "promotion")
						validMovements.append(move)
					else:
						move = Movement(newPos, "normal")
						validMovements.append(move)
					if posT[1] == 2:
						newPos = (posT[0], posT[1]+2)
						try:
							newPos = self.positionTupleFilter(newPos)
							item = self.lookSpecificPosition(newPos)
							if item[0] == "empty":
								move = Movement(newPos, "normal")
								validMovements.append(move)
						except:
							pass
			except:
				pass
			newPos = (posT[0]+1, posT[1]+1)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == otherColor:
					if newPos in ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
						move = Movement(newPos, "promotion")
						validMovements.append(move)
					else:
						move = Movement(newPos, "capture")
						validMovements.append(move)
			except:
				pass
			newPos = (posT[0]-1, posT[1]+1)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == otherColor:
					if newPos in ["a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]:
						move = Movement(newPos, "promotion")
						validMovements.append(move)
					else:
						move = Movement(newPos, "capture")
						validMovements.append(move)
			except:
				pass
			return validMovements


		elif color == "black":
			otherColor = "white"
			try:
				if pos in ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"]:
					newPos = (posT[0]-1, posT[1])
					newPos = self.positionTupleFilter(newPos)
					item = self.lookSpecificPosition(newPos)
					if item == ("white", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == newPos[0] + "2":
							if lastTurn.newPos == newPos[0] + "4":
								newPos = newPos[0] + "3"
								move = Movement(newPos, "passing")
								validMovements.append(move)

					newPos = (posT[0]+1, posT[1])
					newPos = self.positionTupleFilter(newPos)
					item = self.lookSpecificPosition(newPos)
					if item == ("white", "pawn"):
						lastTurn = self.actualTurn - 1
						lastTurn = self.lookSpecificTurn(lastTurn)
						if lastTurn.oldPos == newPos[0] + "2":
							if lastTurn.newPos == newPos[0] + "4":
								newPos = newPos[0] + "3"
								move = Movement(newPos, "passing")
								validMovements.append(move)
			except:
				pass
			newPos = (posT[0], posT[1]-1)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == "empty":
					if newPos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
						move = Movement(newPos, "promotion")
						validMovements.append(move)
					else:
						move = Movement(newPos, "normal")
						validMovements.append(move)
					if posT[1] == 7:
						newPos = (posT[0], posT[1]-2)
						try:
							newPos = self.positionTupleFilter(newPos)
							item = self.lookSpecificPosition(newPos)
							if item[0] == "empty":
								if newPos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
									move = Movement(newPos, "promotion")
									validMovements.append(move)
								else:
									move = Movement(newPos, "normal")
									validMovements.append(move)
						except:
							pass
			except:
				pass
			newPos = (posT[0]+1, posT[1]-1)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == otherColor:
					if newPos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
						move = Movement(newPos, "promotion")
						validMovements.append(move)
					else:
						move = Movement(newPos, "capture")
						validMovements.append(move)
			except:
				pass
			newPos = (posT[0]-1, posT[1]-1)
			try:
				newPos = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(newPos)
				if item[0] == otherColor:
					if newPos in ["a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1"]:
						move = Movement(newPos, "promotion")
						validMovements.append(move)
					else:
						move = Movement(newPos, "capture")
						validMovements.append(move)
			except:
				pass
			return validMovements
		else:
			raise ValueError("Color is invalid")
