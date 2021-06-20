import gym
import random
import numpy as np
import time
from collections import deque
import pickle


from collections import defaultdict


EPISODES =   20000
LEARNING_RATE = .1
DISCOUNT_FACTOR = .99
EPSILON = 1
EPSILON_DECAY = .999



def default_Q_value():
    return 0


if __name__ == "__main__":



    random.seed(1)
    np.random.seed(1)
    env = gym.envs.make("FrozenLake-v0")
    env.seed(1)
    env.action_space.np_random.seed(1)
    

    Q_table = defaultdict(default_Q_value) # starts with a pessimistic estimate of zero reward for each state.

    episode_reward_record = deque(maxlen=100)

    
    def choose_action(state):
      action = 0
      random = np.random.uniform(0,1)
      if random < EPSILON:
        action = env.action_space.sample()
      else:
        prediction = np.array([Q_table[(state,i)] for i in range(env.action_space.n)])
        action =  np.argmax(prediction)
      return action

    
    for i in range(EPISODES):
        episode_reward = 0

        #TODO PERFORM Q LEARNING
        state = env.reset()

        done = False
        
        while done == False:
          
          action = choose_action(state)
          
          state2, reward, done, info = env.step(action)
          
          action2 = choose_action(state2)
          
          episode_reward = episode_reward + reward
          
          if done == False:
            predict = Q_table[(state,action)]
            target = reward + DISCOUNT_FACTOR * np.max(Q_table[(state2,action2)])
            Q_table[(state,action)] = Q_table[(state,action)] + LEARNING_RATE * (target - predict)
          else:
            Q_table[(state,action)] = Q_table[(state,action)] + LEARNING_RATE * (reward - Q_table[(state,action)])
            
          state = state2
          
            
        episode_reward_record.append(episode_reward)
        EPSILON = EPSILON * EPSILON_DECAY
          
        if i%100 ==0 and i>0:
            print(sum(list(episode_reward_record)))
            print("LAST 100 EPISODE AVERAGE REWARD: " + str(sum(list(episode_reward_record))/100))
            print("EPSILON: " + str(EPSILON) )
    
    
    ####DO NOT MODIFY######
    model_file = open('Q_TABLE.pkl' ,'wb')
    pickle.dump([Q_table,EPSILON],model_file)
    #######################







