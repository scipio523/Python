import random

def raffle(n, prizes):
	contestants = list(xrange(1,n+1))
	winners = []
	while len(winners) < 5:
		winner = random.choice(contestants)
		winners.append(winner)
		contestants.remove(winner)
	return winners

print(raffle(10, 5))



