'''
Author: Ruben Dorado

A Python implementation of the CKY algorithm given a CFG and a sentence.
'''
import re

class ParseTree:
	def __init__(self, node):
		self.root = node

	def print(self):
		if self.root != None: self.root.print()


class Node:
	def __init__(self, symbol):
		self.lnode = None
		self.rnode = None
		self.symbol = symbol	
	def print(self,offset=""):
		print( (offset[:-3]+"|--" if len(offset)>0 else "")+str(self.symbol))
		if self.rnode != None: self.rnode.print(offset+"|  ")
		if self.lnode != None: self.lnode.print(offset+"   ")

class Grammar:

	def __init__(self):
		self.rules = {}
		self.terminals = {}
		self.backrule = {}

	def addRule(self, left_side, right_side):
		try:
			self.rules[left_side].append(right_side)
		except KeyError:
			self.rules[left_side] = [right_side]
		try:
			self.backrule[tuple(right_side)].append(left_side)
		except KeyError:
			self.backrule[tuple(right_side)] = [left_side]
		
	def addTerminal(self, left_side, right_side):
		try:
			self.terminals[right_side].append(left_side)
		except KeyError:
			self.terminals[right_side] = [left_side]		

	def print(self):
		print(self.rules)
		print(self.terminals)
		print(self.backrule)
		
	def getTerminalRules(self, terminal):
		resp = ["OOV"]
		try:
			resp = self.terminals[terminal]
		except KeyError: pass 		
		return resp

	def getSymbolFromRule(self, rule):
		resp = []
		try:
			resp = self.backrule[tuple(rule)]
                        
		except KeyError: pass
			
		return resp


def table_print(table):
	for row in table:
		line = ""
		for col in row:
			line+=str(col)+"\t"
		print(line)


def get_parse_tree(state, symbol, table):
	node = Node(symbol)

	state = state[0]
	lsym = state[0]
	rsym = state[1] 

	if lsym[0] != -1:
		node.lnode = get_parse_tree(table[lsym[0]][lsym[1]][lsym[2]],lsym[2],table)
	else:
		node.lnode = Node(lsym[2])

	if len(rsym) > 0:
		node.rnode = get_parse_tree(table[rsym[0]][rsym[1]][rsym[2]],rsym[2],table)

	return node

def cky(grammar, sentence, debug=False):
	n = len(sentence)
	table = [[[] for i in range(n-j)] for j in range(n)]
	unaries = [[{} for i in range(n-j)] for j in range(n)]
	nodes_back = [[{} for i in range(n + 1)] for j in range(n + 1)]

	#Initialize table
	for w in range(1, n + 1):
		symbols = grammar.getTerminalRules(sentence[w-1])
		table[0][w-1].extend( symbols )
		
                # Add unaries 
		for S in symbols:
			rules = grammar.getSymbolFromRule([S])
			try:
				nodes_back[0][w-1][S].append( ((-1,-1,sentence[w-1]),()) )
			except KeyError:
				nodes_back[0][w-1][S] = [ ((-1,-1,sentence[w-1]),()) ]
			for U in rules:
				if U not in unaries[0][w-1] and U not in table[0][w-1]:
					table[0][w-1].append(U)
					unaries[0][w-1][U] = True
					try:
						nodes_back[0][w-1][U].append( ((0,w-1,S),()) )
					except KeyError:
						nodes_back[0][w-1][U] = [ ((0,w-1,S),()) ]

	if debug: table_print(table)
	for l in range(0, n-1):
		for s in range(n-l-1):
			for p in range(l+1):
				for X in table[p][s]:
					for Y in table[l-p][s+p+1]:
						symbols = grammar.getSymbolFromRule([X, Y])
						table[l+1][s].extend(symbols)

                				# Add unaries and backtracks
						for S in symbols:
							try:
								nodes_back[l+1][s][S].append( ((p,s,X),(l-p,s+p+1,Y)) )
							except KeyError:
								nodes_back[l+1][s][S] = [((p,s,X),(l-p,s+p+1,Y))]
							rules = grammar.getSymbolFromRule([S])
							for U in rules:			
								if U not in unaries[l+1][s] and U not in table[l+1][s]:
									table[l+1][s].append(U)
									unaries[l+1][s][U] = True
									nodes_back[l+1][s][U] = ((l+1,s,Y))
		if debug:
			print()				
			table_print(table)

	if 'S' in nodes_back[n-1][0]: return ParseTree( get_parse_tree(nodes_back[n-1][0]['S'], 'S', nodes_back) )
	return None


def load_grammar(grammar_filename):
	grammar = Grammar()
	pattern = re.compile(".+->.+( .+)?")
	
	nline = 0
	with open(grammar_filename, 'r') as f:
		lines = f.readlines()
		for line in lines:
			nline+=1
			line = line.strip()
			if len(line) == 0 or line[0] == '#' : continue
			if not pattern.match(line):
				raise ValueError("Error reading grammar in file '"+grammar_filename+"' line "+nline)
				
			rule = [x.strip() for x in line.split('->')]
			right_side = rule[1].split()

			if len(right_side) == 1 and right_side[0] == right_side[0].lower():
				grammar.addTerminal(rule[0],right_side[0])	
			else:                        
				grammar.addRule(rule[0], right_side)

	return grammar


def parse(grammar_filename, sentence, debug=False):
	grammar = load_grammar(grammar_filename)
	if debug: grammar.print()
	return cky(grammar, sentence.split(),debug=debug)


