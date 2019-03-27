import numpy as np


class BanditEnv(object):

    def __init__(self, topic_rates, default_rate=0.02, num_topics=10000):
        self.topic_rates = topic_rates
        self.default_rate = default_rate
        self.num_topics = num_topics
        self.primes = [7, 23, 73, 97]

    def get_topic_rate(self, topic):
        return self.topic_rates.get(topic, self.default_rate)

    def find_topics(self, doc):
        idx = [(doc%100*p)%100+1 for p in self.primes]
        r = [(i+doc)%self.num_topics for i in idx]
        r.append(doc % self.num_topics)
        return r

    def generate_reward(self, docs):
        result = []
        for doc in docs:
            topics = self.find_topics(doc)
            print('AAA', topics)
            max_r = max([self.get_topic_rate(t) for t in topics])
            print('BBB', max_r)
            reward = np.random.binomial(1, max_r)
            result.append((doc, topics, reward))
        return reward
