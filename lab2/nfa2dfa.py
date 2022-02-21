# John Lovre   - JRL142@pitt.edu
# Suchi Attota - SUA27@pitt.edu
# CS1502
# PA2: NFA to DFA Simulation

# import necessary libraries
import sys, fileinput, os.path, bisect

# NFA Properties
numStates = 0         # size of Q (number of states in set)
alphabet = []         # Sigma
tranFunctions = {}    # [dictionary] delta (qa 'char' qb) => [Q][Sig] -> Q
startState = 0        # qs (initial state of NFA)
acceptStates = []     # F (set of end states that will return "Accept")
#inputStrings = []    # Set of strings tested on NFA


##########################
# Check for input errors #
##########################

# Command line should have 3 arguments (nfa.py and test_case and output_file)
#  Execute format: python3 nfa.py <testcase>.txt <output>.txt
numArgs = len(sys.argv)
if (numArgs != 3):
	sys.exit("INPUT ERROR:\n Format should be \"python3 nfa.py <testcase>.txt <output>.txt\"")

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

inputFile = open(inputFilename, "r")

#  1) read in size of Q (first line of input file)
numStates = int(inputFile.readline())

#  2) read in alphabet (second line of input file)
alphaInput = inputFile.readline()
for eachChar in range(len(alphaInput)):
	alphabet.append(alphaInput[eachChar])
alphabet.remove("\n")

#  3) read in set of transition functions
nextLine = inputFile.readline()
while ("\'" in nextLine):  # each tran function line has 2 ' in it
	# tranFunctions{} is a dictionary of dictionaries
	# format: tranFunctions[source][symbol] = destination
	nextLine = nextLine.replace("\n", "")
	while " " in nextLine:
		nextLine = nextLine.replace(" ", "")
	eachTran = nextLine.split("'")
	source, symbol, dest = eachTran          # read in line as qa, symbol, qb
	source = int(source)
	dest = int(dest)
	if source not in tranFunctions:          # add dictionary entry for source
		tranFunctions[source] = {}
	if symbol not in tranFunctions[source]:  # initialize list for source/symbol
		tranFunctions[source][symbol] = []
	tranFunctions[source][symbol].append(dest)
	nextLine = inputFile.readline()          # repeat for next input line

#  4) read in start state (line after transitions)
nextLine = inputFile.readline() # repeat for next input line
nextLine = nextLine.replace("\n", "")
startState = int(nextLine)

#  5) read in set of accept states
acceptInput = inputFile.readline()
for eachState in acceptInput.split(" "):
	eachState = int(eachState)
	acceptStates.append(eachState)
#	if "" in acceptStates:
#		acceptStates.remove("")
	

#  6) read in set of string inputs
# nextLine = inputFile.readline()
# while (nextLine):
#	if "\n" in nextLine:
#		nextLine = nextLine.replace("\n", "")
#	inputStrings.append(nextLine)
#	nextLine = inputFile.readline();
# destination states in nfa dictionary are going to be sets of destination states in DFA

inputFile.close()


#################
# Next Steps    #
#################
# Now that we know number of state
#  - use number of states
#  - 2 to the power of numStates = total number states in DFA
#  		(the above is max states, not all will get used)
# Hint: use bitfields...
#  array of nfa states (1 by 7, or 7 by 1)
#    -- each entry is going to be 0 or 1
#        (this says...bitfield of NFA states will determine DFA states)


################
# Creating DFA #
################

# DFA Properties
DFAstates = 0            # size of Q (number of states in set)
#alphabet = alphabet     # Alphabet is same for NFA and DFA
DFAtransitions = {}      # [dictionary] delta (qa 'char' qb) => [Q][Sig] -> Q
DFAstartState = 0        # qs (initial state of DFA)
DFAacceptStates = []     # F (set of end states that will return "Accept")
setOfStates = []         # Dictionary of DFA states based on PowerSet(NFA states)

# 1) Create the start state of the DFA, which is E(q0), where q0 is the NFA start state and E(.) is the e-closure)
def eTransitions(NFAstate):
	setofeClosures = []     
	setofeClosures.append(NFAstate)
	if (NFAstate in tranFunctions):
		if ('e' in  tranFunctions[NFAstate]):
			for eclosure in tranFunctions[NFAstate]['e']:
				bisect.insort(setofeClosures, eclosure)
	return setofeClosures
	
def addState(state):
	setOfStates.append(state)
	
# DFA start state = NFA start state and set of states w/in e-closure from start state
addState(eTransitions(startState))
DFAstates = DFAstates + 1
DFAstartState = str(setOfStates[0])

# 2) For every new state R (previous step and every alphabet char delta,
#	(2.a) Compute U(reR)E(delta(r,sigma)) & compute e-closure. Add transtion delt(R,sig) = T
def eClosure(currState):
	setofeClosures = []
	for NFAstate in currState:
		for tran in eTransitions(NFAstate):
			if not (tran in setofeClosures):
				bisect.insort(setofeClosures, tran)
	return setofeClosures

def addTransitions(i):
	DFAtransitions[str(setOfStates[i])] = {}     # Create entry in transitions dictionary for [each] start state
	for symbol in alphabet:                      # and for every alphabet character...
		destinationStates = []                   # ...make a subdictionary entry	
		for state in setOfStates[i]:             # (a) Compute Epsilon closure. 
			if (state in tranFunctions):
				if (symbol in tranFunctions[state]): 
			# Add transitions function of each NFAstate in DFAstates
					for destination in tranFunctions[state][symbol]:
						if not (destination in destinationStates):
							bisect.insort(destinationStates, destination)
			DFAtransitions[DFAstartState][symbol] = destinationStates # ...and here is where it gets put into DFAtransitions
		# (2.b) If DFA did not already have T as state, add it as new state and go back to #2                 
		# Compute e-closure for each state getting added to DFAtransitions
		if not (eClosure(destinationStates) in setOfStates):       # This is where the destination state
			setOfStates.append(eClosure(destinationStates))        # (of transition) gets added to setOfStates[]

i = 0
while i < len(setOfStates):
	addTransitions(i)
	i += 1
	
# 3) Done adding new states when Step two yields no new states
DFAstates = len(setOfStates)


# 4) Make every DFA state that contains NFA state into DFA accept state
#	(only consider states & transitions reachable from start state)


########################
# Write to Output File #
########################
with open(outputFilename, 'w') as outFile:
	outFile.write(str(DFAstates)+'\n')        # Set of States
	for symbol in alphabet:                   # Alphabet
		outFile.write(str(symbol))
	for inState in DFAtransitions:            # Transition Functions
		for inSymbol in alphabet:
		#  1) read-in state
			outFile.write('\n'+inState+" \'")
		#  2) read-in symbol
			outFile.write(inSymbol+"\' ")
		#  3) go-to state
			if (inSymbol in DFAtransitions[inState]):
				outFile.write(str(DFAtransitions[inState][inSymbol]))
	outFile.write('\n'+DFAstartState+'\n')    # Start States
	# TEST BELOW TO WRITES WITH NFA, NEED TO UPDATE TO DFA
	for state in acceptStates:             # Accept States
		outFile.write(str(state)+' ')
	
outFile.close()



#########################################
# Test lines: delete before submitting  #
######################################################################
print()
print("NFA TESTS\n")
print("Test line\n name of test file: " + inputFilename + "\n")
print("Test line\n number of states in NFA: " + str(numStates))
print()
print("Test line\n alphabet: " , alphabet)
print()
print("Test line\n transition functions: ", tranFunctions)
print()
print("Test line\n start state is: " + str(startState) + "\n")
print("Test line\n accept states: " , acceptStates)
print()
#print("Test line \n input strings: " , inputStrings)
#print()
print("\nDFA TESTS")
print("\nTest line\n start state of DFA (e-closures): ")
print(DFAstartState)
# print()
#print()
#print("Test line\n transitions from start state: ")
#for symbol in alphabet:
#	print("on "+symbol+" go to:")
#	print(DFAtransitions[DFAstartState][symbol])
print()
print("Test line\n set of states:")
print(setOfStates)
print()
print("Test line\n DFAtransitions:")
print(DFAtransitions)
print()
######################################################################