
class DataBoard:
	def __init__(self):
		self.validLetters = ["a","b","c","d","e","f","g","h"]
		self.validNumbers = [8,7,6,5,4,3,2,1]
		self.gameState = {}
		self.capturedPieces = {"white": [], "black": []}
		self.initializeGameState()

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
			print("Invalid Piece")
		return validMovements

	def addItemInGameState(self, pos, item):
		self.gameState[pos] = item
	
	def moveItemInGameState(self, oldPos, newPos, color, piece):
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
			validation = newPos in  validMovements
			if validation == False:
				raise RuntimeError("This movement is invalid")
			itemAtNewPos = self.gameState[newPos]
			if itemAtNewPos == ("empty", "empty"):
				pass
			else:
				self.capturedPieces[itemAtNewPos[0]].append(itemAtNewPos[1])
			self.gameState[oldPos] = ("empty", "empty")
			self.gameState[newPos] = item

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
			except Exception as e:
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
			except Exception as e:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
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
					if reachMax == True:
						pass
					else:
						reachMax = True
						validMovements.append(pos)
				else:
					if reachMax == True:
						pass
					else:
						validMovements.append(pos)
			except:
				pass
		return validMovements

	def pawnMovements(self, pos, color):
		posT = self.translatePositionToTuple(pos)
		validMovements = []
		if color == "white":
			otherColor = "black"
			newPos = (posT[0], posT[1]+1)
			try:
				pos1 = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos1)
				if item[0] == "empty":
					validMovements.append(pos1)
				else:
					pass
			except:
				pass
			if posT[1] == 2:
				newPos = (posT[0], posT[1]+2)
				try:
					pos1 = self.positionTupleFilter(newPos)
					item = self.lookSpecificPosition(pos1)
					if item[0] == "empty":
						validMovements.append(pos1)
					else:
						pass
				except:
					pass
			newPos = (posT[0]+1, posT[1]+1)
			try:
				pos1 = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos1)
				if item[0] == otherColor:
					validMovements.append(pos1)
				else:
					pass
			except:
				pass
			newPos = (posT[0]-1, posT[1]+1)
			try:
				pos1 = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos1)
				if item[0] == otherColor:
					validMovements.append(pos1)
				else:
					pass
			except:
				pass
			return validMovements
		elif color == "black":
			otherColor = "white"
			newPos = (posT[0], posT[1]-1)
			try:
				pos1 = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos1)
				if item[0] == "empty":
					validMovements.append(pos1)
				else:
					pass
			except:
				pass
			if posT[1] == 7:
				newPos = (posT[0], posT[1]-2)
				try:
					pos1 = self.positionTupleFilter(newPos)
					item = self.lookSpecificPosition(pos1)
					if item[0] == "empty":
						validMovements.append(pos1)
					else:
						pass
				except:
					pass
			newPos = (posT[0]+1, posT[1]-1)
			try:
				pos1 = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos1)
				if item[0] == otherColor:
					validMovements.append(pos1)
				else:
					pass
			except:
				pass
			newPos = (posT[0]-1, posT[1]-1)
			try:
				pos1 = self.positionTupleFilter(newPos)
				item = self.lookSpecificPosition(pos1)
				if item[0] == otherColor:
					validMovements.append(pos1)
				else:
					pass
			except:
				pass
			return validMovements
		else:
			raise ValueError("Color is invalid")
