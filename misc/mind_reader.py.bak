import os
import sys
import random
import time
import msvcrt as m

def main(threshhold):

	# Initialize dictionaries/lists
	score = {'machine':0, 'human':0, 'winner':''}
	memory = {('WSW','Guess'):'', ('WSW','Repeat'):'', # win, same, win
			  ('WSL','Guess'):'', ('WSL','Repeat'):'', # win, same, lose
			  ('WDW','Guess'):'', ('WDW','Repeat'):'', # win, diff, win
			  ('WDL','Guess'):'', ('WDL','Repeat'):'', # win, diff, lose
			  ('LSW','Guess'):'', ('LSW','Repeat'):'', # lose, same, win
			  ('LSL','Guess'):'', ('LSL','Repeat'):'', # lose, same, lose
			  ('LDW','Guess'):'', ('LDW','Repeat'):'', # lose, diff, win
			  ('LDL','Guess'):'', ('LDL','Repeat'):''} # lose, diff, lose
	pattern,thisResult,thisMachineGuess,thisHumanGuess,lastResult,lastMachineGuess,lastHumanGuess = '','','','','','',''

	# Main game loop
	while not score['winner']:
		# Clear screen and show score
		os.system('cls')
		print 'Machine: '+str(score['machine']) \
			+'	'+'Human: '+str(score['human'])

		# End game if we have a winner
		if score['machine'] >= threshhold: score['winner'] = 'Machine'
		elif score['human'] >= threshhold: score['winner'] = 'Human'
		if score['winner']: break

		# Update variables
		if thisResult: lastResult = thisResult
		if thisMachineGuess: lastMachineGuess = thisMachineGuess
		if thisHumanGuess: lastHumanGuess = thisHumanGuess

		# Prompt player to guess
		print'Guess 1 or 2 aloud.',
		print 'If you guess differently than the machine, you win.',
		print 'Press any key when ready.'
		m.getch() #press any key to continue

		# Generate machine's guess
		if pattern:
			if memory[(pattern,'Repeat')] == 1: # If repeated pattern, assume continuation
				if memory[(pattern,'Guess')] == 'S':
					thisMachineGuess = lastHumanGuess
				else:
					if lastHumanGuess == 1: thisMachineGuess = 2
					else: thisMachineGuess = 1
			else:	# If no repeated pattern, guess randomly
				thisMachineGuess = random.randint(1,2)
		else:
			thisMachineGuess = random.randint(1,2)

		print 'Machine guess: '+str(thisMachineGuess)

		# Collect result
		while True:
			response = raw_input('Did you win? [y/n] ').upper()
			if response in ['Y', 'N']: break
		if response == 'Y': thisResult = 'W' # Convert y/n to w/l
		else: thisResult = 'L' 

		# Increment score
		if thisResult == 'L': score['machine'] += 1
		else: score['human'] += 1 

		# Determine what human guess was
		if thisResult =='W': # human won
			if thisMachineGuess == 1: thisHumanGuess = 2
			else: thisHumanGuess = 1
		else: # human lost
			thisHumanGuess = thisMachineGuess	

		# Determine if human switched
		if not lastResult: continue
		if thisHumanGuess == lastHumanGuess: decision = 'S'
		else: decision = 'D'

		# Update memory
		if pattern:
			# Human repeated pattern
			if memory[(pattern,'Guess')] == decision:
				memory[(pattern,'Repeat')] = 1
			# Human changed pattern
			else:
				memory[(pattern,'Guess')] = decision
				memory[(pattern,'Repeat')] = ''

		# Determine new pattern
		pattern = lastResult+decision+thisResult
	
	print '\nWinner: '+score['winner']+'\n'
	kirbyDance(5)

def kirbyDance(n=2):
	for i in range(n):
		print '^( ^o^ )^' + '\r',
		time.sleep(0.5)
		print '<( ^_^ )>' + '\r',
		time.sleep(0.5)
	print '^( ^_- )>'

main(30)


