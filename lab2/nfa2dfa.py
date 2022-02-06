# 0) Read input from a file as 1st command line argument
#	  -- write output to file as 2nd command line argument
#	(0.a) Read in NFA File
#		(0.a.i) First line of input file: number of states (int)
#		(0.a.ii) Second line of input file: alphabet of NFA
#		(0.a.iii) Thire line and onward: Transition functions (qa 'c' qb)
#		(0.a.iv) Blank line terminates transition function entries
#		(0.a.v) Next line of input file: Start state of NFA (int)
#		(0.a.vi) Last line of input file: Set accept states

# 1) Create start state of DFA (Follow format from Lab1)

# 2) For every new state R (previous step and every alphabet char delta,
#	(2.a) Compute U(reR)E(delta(r,sigma)) & compute e-closure. Add transtion delt(R,sig) = T
#	(2.b) If DFA did not already have T as state, add to new state and go back to 2
# 3) Done adding new states when Step two yields no new states

# 4) Make every DFA state that contains NFA state into DFA accept state
#	(only consider states & transitions reachable from start state)