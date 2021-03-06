# John Lovre   - JRL142@pitt.edu
# Suchi Attota - SUA27@pitt.edu
# CS1502
# PA1: DFA Simulation

# import necessary libraries
import sys, fileinput, os.path

# DFA Properties
numStates = 0         # size of Q (number of states in set)
alphabet = []         # Sigma
tranFunctions = []    # [set of] delta (qa 'char' qb) => (Q x 'Sig' -> Q)
startState = ""       # qs (initial state of DFA)
acceptStates = []     # F (set of end states that will return "Accept")
inputStrings = []     # Set of strings tested on DFA


##########################
# Check for input errors #
##########################

# Command line should have 2 arguments (dfa.py and test_case)
#  Execute format: python3 dfa.py <testcase>.txt
numArgs = len(sys.argv)
if (numArgs != 2):
	sys.exit("INPUT ERROR:\n Format should be \"python3 dfa.py <testcase>.txt\"")

# Check that test file exists
inputFilename = sys.argv[1]
fileExists = os.path.exists(inputFilename)
if (fileExists == False):
	sys.exit("INPUT ERROR:\n Cannot find file. Check spelling of input.")



########################
# Read input from file #
########################
# Note: Program reads in newline (\n) character from input files
#	parsing steps check to remove '\n' from strings and arrays

inputFile = open(inputFilename, "r")

#  1) read in size of Q (first line of input file)
numStates = inputFile.readline()

#  2) read in alphabet (second line of input file)
alphaInput = inputFile.readline()
for eachChar in range(len(alphaInput)):
	alphabet.append(alphaInput[eachChar])
alphabet.remove("\n")

#  3) read in set of transition functions
nextLine = inputFile.readline()
while ("\'" in nextLine):  # each tran function line has 2 ' in it
	# tranFunctions[] is an array of arrays
	# each function in array should be of format: 
	#  [current state, action, next state]
	# separate each item in input line by ' character
	nextLine = nextLine.replace("\n", "")
	while " " in nextLine:
		nextLine = nextLine.replace(" ", "")
	eachTran = nextLine.split("'")
	tranFunctions.append(eachTran)
	nextLine = inputFile.readline() # repeat for next input line

#  4) read in start state (line after transitions)
nextLine = nextLine.replace("\n", "")
startState = nextLine

#  5) read in set of accept states
acceptInput = inputFile.readline()
for eachState in acceptInput.split(" "):
	if "\n" in eachState:
		eachState = eachState.replace("\n", "")
	acceptStates.append(eachState)
	if "" in acceptStates:
		acceptStates.remove("")

#  6) read in set of string inputs
nextLine = inputFile.readline()
while (nextLine):
	if "\n" in nextLine:
		nextLine = nextLine.replace("\n", "")
	inputStrings.append(nextLine)
	nextLine = inputFile.readline();

inputFile.close()


######################
# DFA Trace Function #
######################
# Initialize state at qs, read in input string,
#  and jump to next state based on transition functions

def dfaTrace(input):
	# Break down input string into character array
	#  and set current state at start of DFA
	inputArray = [char for char in input]
	currState = startState

	# Based on transition function,
	#  set current state to new state
	for eachChar in inputArray:
		# 1) what is current state?
		# 2) what is current char?
		# 3) based on 1 and 2 above, what state comes next?
		for eachTran in tranFunctions:
			if (eachTran[0]==currState and eachTran[1]==eachChar):
				currState = eachTran[2]
				break

	# Print if we finished on an accept or reject state
	if(currState in acceptStates):
		print("Accept")
	else:
		print("Reject")


##########
# Output #
##########
#  Run "dfaTrace()" on each string in inputString array,
#   should print either "Accept" or "Reject"
for eachString in inputStrings:
	dfaTrace(eachString)