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
	def _init_(self, numStates, alphabet, tranFunctions, startState, acceptStates):
		self.numStates = numStates
		self.alphabet = alphabet
		self.tranFunctions = tranFunctions
		self.startState = startState
		self.acceptStates = acceptStates

class DFA:
	def _init_(self, numStates, alphabet, tranFunctions, startState, acceptStates):
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

# 1)The alphabet of the language appears by itself on the fist line of the input file. Every
#	character in the line (not including the terminating newline character, or any space
#	characters) is a symbol of the alphabet. The alphabet cannot include the letter e,
#	the letter N, the symbol *, the symbol j, or the left or right parenthesis, as these
#	have specific meanings in the regular expressions.
alphaInput = inputFile.readline()
for eachChar in range(len(alphaInput)):
	alphabet.append(alphaInput[eachChar])
alphabet.remove("\n")

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
print("Test line\n name of test file: " + inputFilename)
#print()
print("Test line\n regex: " + regex)
#print()
print("Test line\n alphabet: " , alphabet)
#print()
print("Test line \n input strings: " , inputStrings)
print()
######################################################################
