"""
Reinforcement learning maze example.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

from maze_env import Maze
from RL_brain import QLearningTable

episodes = 100

def update():
    for episode in range(episodes):
        # initial observation
        state = env.reset()
        score = 1.0

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(state))

            # RL take action and get next observation and reward
            state_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(state), action, reward, str(state_))

            score += reward

            # break while loop when end of this episode
            if done:
            	print('Iteration:', episode+1, 'Score:', score)
            	break

            # swap observation
            state = state_

    # end of game
    print('game over')
    env.destroy()

if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(0, update)
    env.mainloop()