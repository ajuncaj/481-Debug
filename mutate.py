import ast
import astor
import sys
import pdb
import copy
import random

#TO-DO:
# Decide when/how to create mutants
# Test mutants (public tests, pylint, 
# Add more/more "creative" mutations

#Initial Counters
totalNodes = 0
numOps = 0
numComps = 0
numCalls = 0
numAssigns = 0
#Running Counters

class MyVisitor(ast.NodeTransformer):

	def __init__(self, opsIn, compsIn, callsIn):
		self.runningOps = 0
		self.runningComps = 0
		self.runningCalls = 0

		self.opsIn = opsIn 
		self.compsIn = compsIn
		self.callsIn = callsIn
		if (opsIn == 0):
			self.changeOps = 0
		else:
			self.changeOps = random.randrange(0, opsIn)
		if (compsIn == 0):
			self.changeComps = 0
		else:
			self.changeComps = random.randrange(0, compsIn)
		if (callsIn == 0):
			self.changeCalls = 0
		else:
			self.changeCalls = random.randrange(0, callsIn)

	# <------ BINARY OPS ------> #
	def visit_Add(self, node):
				
		if (self.runningOps == self.changeOps):
			self.runningOps += 1
			newNode = ast.Sub()
			return newNode
		self.runningOps += 1
		return node
		
	def visit_Sub(self, node):
			
		if (self.runningOps == self.changeOps):
			self.runningOps += 1
			newNode = ast.Add()
			return newNode
		self.runningOps += 1
		return node

	def visit_Mult(self, node):
			
		if (self.runningOps == self.changeOps):
			self.runningOps += 1			
			newNode = ast.FloorDiv()
			return newNode
		self.runningOps += 1
		return node

	def visit_FloorDiv(self, node):	
		
		if (self.runningOps == self.changeOps):
			self.runningOps += 1			
			newNode = ast.Mult()
			return newNode
		self.runningOps += 1
		return node

	def visit_Div(self, node):
		
		if (self.runningOps == self.changeOps):
			self.runningOps += 1			
			newNode = ast.Mult()
			return newNode
		self.runningOps += 1		
		return node
	# <------ BINARY OPS ------> #


	# <------ COMPARISONS ------> #
	def visit_Eq(self, node):

		if (self.runningComps == self.changeComps):
			self.runningComps += 1					
			newNode = ast.NotEq()
			return newNode
		self.runningComps += 1				
		return node

	def visit_NotEq(self, node):
	
		if (self.runningComps == self.changeComps):
			self.runningComps += 1					
			newNode = ast.Eq()
			return newNode
		self.runningComps += 1				
		return node

	def visit_Lt(self, node):
	
		if (self.runningComps == self.changeComps):
			self.runningComps += 1					
			newNode = ast.GtE()
			return newNode
		self.runningComps += 1				
		return node

	def visit_LtE(self, node):

		if (self.runningComps == self.changeComps):
			self.runningComps += 1					
			newNode = ast.Gt()
			return newNode
		self.runningComps += 1				
		return node

	def visit_Gt(self, node):

		if (self.runningComps == self.changeComps):
			self.runningComps += 1					
			newNode = ast.LtE()
			return newNode
		self.runningComps += 1				
		return node

	def visit_GtE(self, node):
		
		if (self.runningComps == self.changeComps):
			self.runningComps += 1					
			newNode = ast.Lt()
			return newNode
		self.runningComps += 1				
		return node

	# <------ COMPARISONS ------> #


	# <------ ASSIGNMENTS + FUNCTIONS ------> #
	
	def visit_Assign(self, node):
		
		newNode = ast.Expr(ast.Num(1))
		return node

	def visit_Call(self, node):
			
		if (self.runningCalls == self.changeCalls):
			self.runningCalls += 1				
			newNode =  ast.Expr(ast.Num(1))
			return newNode
		self.runningCalls += 1	
		return node

	# <------ ASSIGNMENTS + FUNCTIONS ------> #

	# <------ HELPERS ------> #
	
	# gets new random numbers for a new mutant		
	def refresh(self):
		self.runningOps = 0
		self.runningComps = 0
		self.runningCalls = 0	
		self.changeOps = random.randrange(0, self.opsIn)
		self.changeComps = random.randrange(0, self.compsIn)
		self.changeCalls = random.randrange(0, self.callsIn)

	# <------ HELPERS ------> #

class FirstVisitor(ast.NodeVisitor):
#Small visitor to gather info on initial program
	def visit_Call(self, node):
		global totalNodes		
		global numCalls		
		
		totalNodes += 1
		numCalls += 1

	def visit_Compare(self, node):
		global totalNodes		
		global numComps			

		totalNodes += 1
		numComps += 1

	def visit_BinOp(self, node):
		global totalNodes		
		global numOps

		totalNodes += 1
		numOps += 1

# sys.argv[1] = program
# sys.argv[2] = # mutants
	
def main():
	print("reached begining of main()")
	numMutants = int(sys.argv[2])
	random.seed(42069420)

	with open(sys.argv[1], "r") as source:
		tree = ast.parse(source.read())

	# Run FirstVisitor to get info on what to mutate
	visitor = FirstVisitor()
	visitor.visit(tree)
	print("successfully ran first visitor")	
	
	visitor = MyVisitor(numOps, numComps, numCalls)
	# Loop numMutant times to make numMutant new files. Copy tree each time to get new mutants
	for i in range(numMutants):
		treeCopy = copy.deepcopy(tree)	
		visitor.visit(treeCopy)
		ast.fix_missing_locations(treeCopy)

		fileName = ".txt"
		f = open(str(i)+fileName, "w")
		f.write(astor.to_source(treeCopy))

		visitor.refresh()
		print("mutant created")

	print("done!")
if __name__ == '__main__': main()

