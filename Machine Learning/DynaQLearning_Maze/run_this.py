"""
Simplest model-based RL, Dyna-Q.

Red rectangle:          explorer.
Black rectangles:       hells       [reward = -1].
Yellow bin circle:      paradise    [reward = +1].
All other states:       ground      [reward = 0].

This script is the main part which controls the update method of this example.
The RL is in RL_brain.py.

View more on my tutorial page: https://morvanzhou.github.io/tutorials/
"""

from maze_env import Maze
from RL_brain import QLearningTable, EnvModel

episodes = 40
sim_episodes = 10

def update():
    for episode in range(episodes):
        s = env.reset()
        score = 1.0

        while True:
            env.render()

            # Choose action based on current state
            a = RL.choose_action(str(s))

            # Find new state and reward 
            s_, r, done = env.step(a)

            # Update Q Table based on experience
            RL.learn(str(s), a, r, str(s_))

            # use a model to output (r, s_) by inputting (s, a)
            # the model in dyna Q version is just like a memory replay buffer
            env_model.store_transition(str(s), a, r, s_)
            for n in range(sim_episodes):  # learn 10 more times using the env_model
                ms, ma = env_model.sample_s_a()  # ms in here is a str
                mr, ms_ = env_model.get_r_s_(ms, ma)
                RL.learn(ms, ma, mr, str(ms_))

            score += r

            # break while loop when end of this episode
            if done:
                print('Iteration:', episode+1, 'Score:', score)
                break

            s = s_

    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    env = Maze()
    RL = QLearningTable(actions=list(range(env.n_actions)))
    env_model = EnvModel(actions=list(range(env.n_actions)))

    env.after(0, update)
    env.mainloop()