import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import pandas as pd
import seaborn as sns
import gym
import numpy
import math
import os
import random

import cntk as C


isFast = True
C.device.try_set_default_device(C.device.gpu(0))


env = gym.make('CartPole-v0')

STATE_COUNT  = env.observation_space.shape[0]
ACTION_COUNT = env.action_space.n

print("State count", STATE_COUNT, "action count", ACTION_COUNT)

# Targetted reward
REWARD_TARGET = 30 if isFast else 200
# Averaged over these these many episodes
BATCH_SIZE_BASELINE = 20 if isFast else 50

H = 64 # hidden layer size

class Brain:
    def __init__(self):
        self.params = {}
        self.model, self.trainer, self.loss = self._create()
        # self.model.load_weights("cartpole-basic.h5")

    def _create(self):
        observation = C.sequence.input_variable(STATE_COUNT, np.float32, name="s")
        q_target = C.sequence.input_variable(ACTION_COUNT, np.float32, name="q")

        # Following a style similar to Keras
        l1 = C.layers.Dense(H, activation=C.relu)
        l2 = C.layers.Dense(ACTION_COUNT)
        unbound_model = C.layers.Sequential([l1, l2])
        model = unbound_model(observation)

        self.params = dict(W1=l1.W, b1=l1.b, W2=l2.W, b2=l2.b)

        # loss='mse'
        loss = C.reduce_mean(C.square(model - q_target), axis=0)
        meas = C.reduce_mean(C.square(model - q_target), axis=0)

        # optimizer
        lr = 0.00025
        lr_schedule = C.learning_parameter_schedule(lr)
        learner = C.sgd(model.parameters, lr_schedule, gradient_clipping_threshold_per_sample=10)
        trainer = C.Trainer(model, (loss, meas), learner)

        # CNTK: return trainer and loss as well
        return model, trainer, loss

    def train(self, x, y, epoch=1, verbose=0):
        #self.model.fit(x, y, batch_size=64, nb_epoch=epoch, verbose=verbose)
        arguments = dict(zip(self.loss.arguments, [x,y]))
        updated, results =self.trainer.train_minibatch(arguments, outputs=[self.loss.output])

    def predict(self, s):
        return self.model.eval([s])


class Memory:   # stored as ( s, a, r, s_ )
    samples = []

    def __init__(self, capacity):
        self.capacity = capacity

    def add(self, sample):
        self.samples.append(sample)

        if len(self.samples) > self.capacity:
            self.samples.pop(0)

    def sample(self, n):
        n = min(n, len(self.samples))
        return random.sample(self.samples, n)


MEMORY_CAPACITY = 100000
BATCH_SIZE = 64

GAMMA = 0.99 # discount factor

MAX_EPSILON = 1
MIN_EPSILON = 0.01 # stay a bit curious even when getting old
LAMBDA = 0.0001    # speed of decay

class Agent:
    steps = 0
    epsilon = MAX_EPSILON

    def __init__(self):
        self.brain = Brain()
        self.memory = Memory(MEMORY_CAPACITY)

    def act(self, s):
        if random.random() < self.epsilon:
            return random.randint(0, ACTION_COUNT-1)
        else:
            return numpy.argmax(self.brain.predict(s))

    def observe(self, sample):  # in (s, a, r, s_) format
        self.memory.add(sample)

        # slowly decrease Epsilon based on our eperience
        self.steps += 1
        self.epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * math.exp(-LAMBDA * self.steps)

    def replay(self):
        batch = self.memory.sample(BATCH_SIZE)
        batchLen = len(batch)

        no_state = numpy.zeros(STATE_COUNT)


        # CNTK: explicitly setting to float32
        states = numpy.array([ o[0] for o in batch ], dtype=np.float32)
        states_ = numpy.array([(no_state if o[3] is None else o[3]) for o in batch ], dtype=np.float32)
        print('AAA states', states)
        print('AAA states_', states_)

        p = self.brain.predict(states)
        print('AAA p is', p)
        p_ = self.brain.predict(states_)
        print('AAA p_ is', p_)

        # CNTK: explicitly setting to float32
        x = numpy.zeros((batchLen, STATE_COUNT)).astype(np.float32)
        y = numpy.zeros((batchLen, ACTION_COUNT)).astype(np.float32)

        for i in range(batchLen):
            s, a, r, s_ = batch[i]

            # CNTK: [0] because of sequence dimension
            t = p[0][i]
            if s_ is None:
                t[a] = r
            else:
                t[a] = r + GAMMA * numpy.amax(p_[0][i])
            print('AAA t', t)

            x[i] = s
            y[i] = t

        self.brain.train(x, y)


def plot_weights(weights, figsize=(7, 5)):
    '''Heat map of weights to see which neurons play which role'''
    sns.set(style="white")
    f, ax = plt.subplots(len(weights), figsize=figsize)
    cmap = sns.diverging_palette(220, 10, as_cmap=True)

    for i, data in enumerate(weights):
        axi = ax if len(weights) == 1 else ax[i]
        if isinstance(data, tuple):
            w, title = data
            axi.set_title(title)
        else:
            w = data

        sns.heatmap(w.asarray(), cmap=cmap, square=True, center=True,  # annot=True,
                    linewidths=.5, cbar_kws={"shrink": .25}, ax=axi)

def epsilon(steps):
    return MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * np.exp(-LAMBDA * steps)

plt.plot(range(10000), [epsilon(x) for x in range(10000)], 'r')
plt.xlabel('step');plt.ylabel('$\epsilon$')


TOTAL_EPISODES = 2000 if isFast else 3000

def run(agent):
    s = env.reset()
    R = 0

    while True:
        # Uncomment the line below to visualize the cartpole
        # env.render()

        # CNTK: explicitly setting to float32
        a = agent.act(s.astype(np.float32))

        s_, r, done, info = env.step(a)

        if done: # terminal state
            s_ = None

        agent.observe((s, a, r, s_))
        agent.replay()

        s = s_
        R += r

        if done:
            return R

agent = Agent()

episode_number = 0
reward_sum = 0
while episode_number < TOTAL_EPISODES:
    reward_sum += run(agent)
    episode_number += 1
    if episode_number % BATCH_SIZE_BASELINE == 0:
        print('Episode: %d, Average reward for episode %f.' % (episode_number,
                                                               reward_sum / BATCH_SIZE_BASELINE))
        if episode_number%200==0:
            plot_weights([(agent.brain.params['W1'], 'Episode %i $W_1$'%episode_number)], figsize=(14,5))
        if reward_sum / BATCH_SIZE_BASELINE > REWARD_TARGET:
            print('Task solved in %d episodes' % episode_number)
            plot_weights([(agent.brain.params['W1'], 'Episode %i $W_1$'%episode_number)], figsize=(14,5))
            break
        reward_sum = 0
agent.brain.model.save('dqn.mod')