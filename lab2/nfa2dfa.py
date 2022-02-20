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
alphabet = alphabet      # Alphabet is same for NFA and DFA
DFAtransitions = {}      # [dictionary] delta (qa 'char' qb) => [Q][Sig] -> Q
DFAstartState = 0        # qs (initial state of DFA)
DFAacceptStates = []     # F (set of end states that will return "Accept")

# 1) Create the start state of the DFA, which is E(q0), where q0 is the NFA start state and E(.) is the e-closure)
setofeClosures = []     # DFA start state = NFA start state and set of states w/in e-closure from start state
setofeClosures.append(startState)
if ('e' in  tranFunctions[startState]):     # Need to test if there are epsilon transitions or else will break
	for eclosure in tranFunctions[startState]['e']:
		bisect.insort(setofeClosures, eclosure)
DFAstartState = str(setofeClosures)  # this is not correct, but here just for the time being
DFAstates = DFAstates + 1

# 2) For every new state R (previous step and every alphabet char delta,
#	(2.a) Compute U(reR)E(delta(r,sigma)) & compute e-closure. Add transtion delt(R,sig) = T
DFAtransitions[DFAstartState] = {}
for symbol in alphabet:
	destinationStates = []
	for state in setofeClosures:
		if (symbol in tranFunctions[state]):
			for destination in tranFunctions[state][symbol]:
				bisect.insort(destinationStates, destination)
	DFAtransitions[DFAstartState][symbol] = str(destinationStates)

	
#	(2.b) If DFA did not already have T as state, add to new state and go back to 2
# 3) Done adding new states when Step two yields no new states


# 4) Make every DFA state that contains NFA state into DFA accept state
#	(only consider states & transitions reachable from start state)


########################
# Write to Output File #
########################
with open(outputFilename, 'w') as outFile:
	outFile.write(str(DFAstates)+'\n')        # Set of States
	for symbol in alphabet:                   # Alphabet
		outFile.write(str(symbol))
	# This is a test on NFA tran Functions
	# NEED TO SWAP OUT tranFunctions to DFAtransitions
	for inState in tranFunctions:             # Transition Functions
		for inSymbol in tranFunctions[inState]:
		#  1) read-in state
			outFile.write('\n'+str(inState)+" \'")
		#  2) read-in symbol
			outFile.write(inSymbol+"\' ")
		#  3) go-to state
			outFile.write(str(tranFunctions[inState][inSymbol]))
	outFile.write('\n'+str(DFAstartState)+'\n')    # Start States
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
print(setofeClosures)
print()
print("Test line\n transitions from start state: ")
for symbol in alphabet:
	print("on "+symbol+" go to:")
	print(DFAtransitions[DFAstartState][symbol])
	print()
######################################################################
