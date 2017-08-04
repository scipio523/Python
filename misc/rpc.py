import os
import sys
import random
import time
import msvcrt as m

def main(threshhold):

	# Initialize dictionaries/lists/variables
	score = {'machine':0, 'human':0, 'winner':''}
	memory = {('WSW','Guess'):'', ('WSW','Repeat'):'', # win, same, win
			  ('WSL','Guess'):'', ('WSL','Repeat'):'', # win, same, lose
			  ('WST','Guess'):'', ('WST','Repeat'):'', # win, same, tie
			  ('WDW','Guess'):'', ('WDW','Repeat'):'', # win, diff, win
			  ('WDL','Guess'):'', ('WDL','Repeat'):'', # win, diff, lose
			  ('WDT','Guess'):'', ('WDT','Repeat'):'', # win, diff, tie
			  ('LSW','Guess'):'', ('LSW','Repeat'):'', # lose, same, win
			  ('LSL','Guess'):'', ('LSL','Repeat'):'', # lose, same, lose
			  ('LST','Guess'):'', ('LST','Repeat'):'', # lose, same, tie
			  ('LDW','Guess'):'', ('LDW','Repeat'):'', # lose, diff, win
			  ('LDL','Guess'):'', ('LDL','Repeat'):'', # lose, diff, lose
			  ('LDT','Guess'):'', ('LDT','Repeat'):'', # lose, diff, tie
			  ('TSW','Guess'):'', ('TSW','Repeat'):'', # tie, same, win
			  ('TSL','Guess'):'', ('TSL','Repeat'):'', # tie, same, lose
			  ('TST','Guess'):'', ('TST','Repeat'):'', # tie, same, tie
			  ('TDW','Guess'):'', ('TDW','Repeat'):'', # tie, diff, win
			  ('TDL','Guess'):'', ('TDL','Repeat'):'', # tie, diff, lose
			  ('TDT','Guess'):'', ('TDT','Repeat'):''} # tie, diff, tie
	pattern,thisResult,thisMachineGuess,thisHumanGuess,lastResult,lastMachineGuess,lastHumanGuess = '','','','','','',''
	choiceList = ['rock','paper','scissors']

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
		print'Choose rock, paper, or scissors. Say your choice aloud.'
		print 'Press any key when ready. '
		m.getch() #press any key to continue

		# Generate machine's guess
		if pattern:
			if memory[(pattern,'Repeat')] == 1: # If repeated pattern, assume continuation
				if memory[(pattern,'Guess')] == 'S': # Predict human to play same as last time
					if lastHumanGuess == 'rock': thisMachineGuess = 'paper'
					elif lastHumanGuess == 'paper': thisMachineGuess = 'scissors'
					else: thisMachineGuess = 'rock'
				else: # Predict human to play different than last time
					thisChoiceList = choiceList[:]
					if lastHumanGuess == 'rock': thisChoiceList.remove('paper')
					elif lastHumanGuess == 'paper': thisChoiceList.remove('scissors')
					else: thisChoiceList.remove('rock')
					thisMachineGuess = random.choice(thisChoiceList)
			else: # If no repeated pattern, guess randomly
				thisMachineGuess = random.choice(choiceList)
		else:
			thisMachineGuess = random.choice(choiceList)
		print 'Machine guess: '+str(thisMachineGuess)

		# Collect result
		while True:
			thisResult = raw_input('\nDid you win, lose, or tie? [W/L/T] ').upper()
			if thisResult in ['W', 'L', 'T']: break

		# Increment score
		if thisResult == 'L': score['machine'] += 1
		elif thisResult == 'W': score['human'] += 1 

		# Determine what human guess was
		if thisResult == 'T': thisHumanGuess = thisMachineGuess # Tie
		elif thisResult == 'W': # Human won
			if thisMachineGuess == 'rock': thisHumanGuess = 'paper'
			elif thisMachineGuess == 'paper': thisHumanGuess = 'scissors'
			else: thisHumanGuess = 'rock'
		else: # Human lost
			if thisMachineGuess == 'rock': thisHumanGuess = 'scissors'
			elif thisMachineGuess == 'paper': thisHumanGuess = 'rock'
			else: thisHumanGuess = 'paper'

		# Determine if human switched
		if not lastHumanGuess: continue # skip first run
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

main(50)


