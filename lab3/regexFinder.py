# John Lovre   - JRL142@pitt.edu
# Suchi Attota - SUA27@pitt.edu
# CS1502
# PA3: Regex Pattern Recognition

# 0) For this program you will read an alphabet and a regular expression from a file, and then
# 	determine if a series of strings belong to the language of the regular expression. You will do
# 	this by implementing the following algorithm:

# 1) Convert the regular expression to an equivalent NFA, using the algorithm described in
# 	class and in the textbook.

# 2) Convert the NFA into an equivalent DFA, using the algorithm described in class and
# 	in the textbook. Here, you can use the code you wrote for PA2, but you will not write
# 	the DFA to a file - keep it in memory.

# 3) For each of the strings, determine if it is in the language of the DFA by simulating the
# 	DFA on the string. Here, you can use the code you wrote of PA1, but you will get the
# 	DFA from memory, and not from a file. You will write the results to a file, which will
# 	have one line per string, indicating if the string is ("true") or is not ("false") in the
#	language of the regular expression.

# import necessary libraries
import sys, fileinput, os.path, bisect

# global variables
alphabet = []      # used for regex, NFA, and DFA
regex = ""         # will be converted to an NFA, and then a DFA
inputStrings = []  # set of strings tested on DFA

# define data structures
class NFA: 
	def __init__(self, numStates, alphabet, tranFunctions, startState, acceptStates):
		self.numStates = numStates
		self.alphabet = alphabet
		self.tranFunctions = tranFunctions
		self.startState = startState
		self.acceptStates = acceptStates

class DFA:
	def __init__(self, numStates, alphabet, tranFunctions, startState, acceptStates):
		self.numStates = numStates
		self.alphabet = alphabet
		self.tranFunctions = tranFunctions
		self.startState = startState
		self.acceptStates = acceptStates


# The program should read input from a file that is specifed as the first com-
# mand line argument to the program, and write output to a file whose name is
# specified as the second command line argument to the program. The program
# should not prompt the user for interactive input.

##########################
# Check for input errors #
##########################
# Command line should have 3 arguments (regexFinder.py, test_case, and output_file)
#  Execute format: python3 regexFinder.py <testcase>.txt <output>.txt
numArgs = len(sys.argv)
if (numArgs != 3):
	sys.exit("INPUT ERROR:\n Format should be \"python3 regexFinder.py <testcase>.txt <output>.txt\"")

# Check that test file exists
inputFilename = sys.argv[1]
fileExists = os.path.exists(inputFilename)
if (fileExists == False):
	sys.exit("INPUT ERROR:\n Cannot find file. Check spelling of input.")

# Create output file
outputFilename = sys.argv[2]


########################
# Read input from file #
########################
# Note: Program reads in newline (\n) character from input files
#	parsing steps check to remove '\n' from strings and arrays

#  0) The input file name is the first command line argument.
inputFile = open(inputFilename, "r")

# 1)The alphabet of the language appears by itself on the fist line of the input file.
alphaInput = inputFile.readline()          # Every character in the line (not including the terminating newline character, or any space
for eachChar in range(len(alphaInput)):    # characters) is a symbol of the alphabet. The alphabet cannot include the letter e,
	alphabet.append(alphaInput[eachChar])  # the letter N, the symbol *, the symbol j, or the left or right parenthesis, as these
alphabet.remove("\n")                      # have specific meanings in the regular expressions.

# 2) A regular expression appears by itself on the second line of the input file.
nextLine = inputFile.readline()
regex = nextLine.replace("\n", "")

#  3) Following the regular expressions are a sequence of strings, one per line for the remain-
#	der of the input file.
nextLine = inputFile.readline()
while (nextLine):
	if "\n" in nextLine:
		nextLine = nextLine.replace("\n", "")
	inputStrings.append(nextLine)
	nextLine = inputFile.readline();

inputFile.close()


############################################################################################
# 1) Convert the regular expression to an equivalent NFA, using the algorithm described in #
# 	class and in the textbook.                                                             #
############################################################################################
myNFA = {}

#<conversion code goes here>#

#<...in the meantime...dummy variables below>###################################
numStates = 0         # size of Q (number of states in set)
#alphabet = []         # Sigma
tranFunctions = {}    # [dictionary] delta (qa 'char' qb) => [Q][Sig] -> Q
startState = 0        # qs (initial state of NFA)
acceptStates = []  # F (set of end states that will return "Accept")
#<end dummy variables block>####################################################

myNFA = NFA(numStates, alphabet, tranFunctions, startState, acceptStates)



###########################################################################################
# 2) Convert the NFA into an equivalent DFA, using the algorithm described in class and   #
# 	in the textbook. Here, you can use the code you wrote for PA2, but you will not write #
# 	the DFA to a file - keep it in memory.                                                #
###########################################################################################

myDFA = {}

def nfa2dfa(thisNFA):
	
	# DFA Properties
	DFAstates = 0            # size of Q (number of states in set)
	#alphabet = alphabet     # Alphabet is same for NFA and DFA
	DFAtransitions = {}      # [dictionary] delta (qa 'char' qb) => [Q][Sig] -> Q
	DFAstartState = 0        # qs (initial state of DFA)
	DFAacceptStates = []     # F (set of end states that will return "Accept")
	setOfStates = []         # Dictionary of DFA states based on PowerSet(NFA states)

	# 2.1) Create the start state of the DFA, which is E(q0), where q0 is the NFA start state and E(.) is the e-closure)
	def eTransitions(NFAstate):
		setofeClosures = []     
		setofeClosures.append(NFAstate)
		if (NFAstate in thisNFA.tranFunctions):
			if ('e' in  thisNFA.tranFunctions[NFAstate]):
				for eclosure in thisNFA.tranFunctions[NFAstate]['e']:
					bisect.insort(setofeClosures, eclosure)
		return setofeClosures

	def eClosure(DFAState):
		setofeClosures = []
		for NFAstate in DFAState:
			for tran in eTransitions(NFAstate):
				if not (tran in setofeClosures):
					bisect.insort(setofeClosures, tran)
		return setofeClosures
		
	def addState(DFAstate):
		if not (DFAstate in setOfStates):    # only add if state not already in data structure
			setOfStates.append(DFAstate)
			
	# DFA start state = NFA start state and set of states w/in e-closure from start state
	DFAstartState = eClosure(eTransitions(thisNFA.startState))
	addState(DFAstartState)

	# 2.2) For every new state R (previous step and every alphabet char delta,
	#	(2.2.a) Compute U(reR)E(delta(r,sigma)) & compute e-closure. Add transtion delt(R,sig) = T
	def addTransitions(i):
		currState = str(setOfStates[i])
		DFAtransitions[currState] = {}     
	# Create entry in transitions dictionary for [each] start state
		for symbol in alphabet:              # and for every alphabet character...
			destinationStates = []           # ...make a subdictionary entry	
		# (a) Compute Epsilon closure. 
			for state in setOfStates[i]:     
				if (state in thisNFA.tranFunctions):
					if (symbol in thisNFA.tranFunctions[state]): 
		# Add transitions function of each NFAstate in DFAstates array...
						for destination in thisNFA.tranFunctions[state][symbol]:
							if not (destination in destinationStates):
								bisect.insort(destinationStates, destination)
		# Compute e-closure for each state getting added to DFAtransitions
			destinationStates = (eClosure(destinationStates))
		# ...and add this to the transition functions	
			DFAtransitions[currState][symbol] = destinationStates 

		# (2.2.b) If DFA did not already have T as state, add it as new state and go back to #2                 
			addState(destinationStates)      # addState() automatically checks for duplicates

	# Loop through set of DFA states 
	# and add transitions and states as needed
	stateCounter = 0
	while stateCounter < len(setOfStates):
		addTransitions(stateCounter)
		stateCounter += 1

	# 2.3) Done adding new states when Step two yields no new states
	DFAstates = len(setOfStates)

	# 2.4) Make every DFA state that contains NFA state into DFA accept state
	#	(only consider states & transitions reachable from start state)
	for eachAccept in thisNFA.acceptStates:
		for eachState in setOfStates:
			for eachNFA in eachState:
				if (eachAccept == eachNFA):
					DFAacceptStates.append(setOfStates.index(eachState) + 1)


# need to add conversion of set of state and transition funciton arrays

	return DFA(DFAstates, alphabet, DFAtransitions, DFAstartState, DFAacceptStates)

# Run nfa2dfa on our nfa from earlier
myDFA = nfa2dfa(myNFA)


###############################################################################################
# 3) For each of the strings, determine if it is in the language of the DFA by simulating the #
# 	DFA on the string. Here, you can use the code you wrote of PA1, but you will get the      #
# 	DFA from memory, and not from a file. You will write the results to a file, which will    #
# 	have one line per string, indicating if the string is ("true") or is not ("false") in the #
#	language of the regular expression.                                                       #
###############################################################################################

#<code here>#



########################
# Write to Output File #
########################

# 0) The output file name is the second command line argument.
#with open(outputFilename, 'w') as outFile:

# 1) Your program should write true or false for each string in the input file,
# 	true if the string is in the language described by the regular expression,
# 	and false if not. The output file should contain one true or false value per
# 	line.

# 2) If an invalid regular expression is encountered, your program should print
# 	"Invalid expression" to the output file on a single line. Nothing else should
# 	be printed to the file.
	

#outFile.close()




#########################################
# Test lines: delete before submitting  #
######################################################################
print()
print("\nRegex Tests\n")
print("Test line\n name of test file: " + inputFilename)
#print()
print("Test line\n regex: " + regex)
#print()
print("Test line\n alphabet: " , alphabet)
#print()
print("Test line \n input strings: " , inputStrings)
print()
print("\nNFA Tests\n")
print("Test line\n NFA numState: "+str(myNFA.numStates))
#print()
print("Test line\n NFA alphabet: "+str(myNFA.alphabet))
#print()
print("Test line\n NFA tranFunctions: "+str(myNFA.tranFunctions))
#print()
print("Test line\n NFA startState: "+str(myNFA.startState))
#print()
print("Test line\n NFA acceptState: "+str(myNFA.acceptStates))
print()
print("\nDFA Tests\n")
print("Test line\n DFA numState: "+str(myDFA.numStates))
#print()
print("Test line\n DFA alphabet: "+str(myDFA.alphabet))
#print()
print("Test line\n DFA tranFunctions: "+str(myDFA.tranFunctions))
#print()
print("Test line\n DFA startState: "+str(myDFA.startState))
#print()
print("Test line\n DFA acceptState: "+str(myDFA.acceptStates))
print()
######################################################################
