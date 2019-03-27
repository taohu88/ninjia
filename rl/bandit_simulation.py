import math
from anytree import Node, RenderTree, Resolver
from collections import deque
import numpy as np
from bandit_env import BanditEnv


class ExNode(Node):
    def __init__(self, name, parent=None, **kwargs):
        super(self.__class__, self).__init__(name, parent, **kwargs)
        self.agg_r = 0.0
        self.agg_seens = 0.0
        self.r = 0.0
        self.seens = 0.0

    def inc_update_self(self, r, delta_seens=1.0, alpha=0.9):
        self.r = self.r * alpha + r * (1.0 - alpha)
        self.seens += delta_seens

        if self.is_leaf:
            # they are same
            self.agg_r = self.r
            self.agg_seens = self.seens
        else:
            self.agg_r = max(self.agg_r, self.r)
            self.agg_seens += delta_seens

    def inc_update(self, r, delta_seens=1.0, alpha=0.9):
        self.inc_update_self(r, delta_seens, alpha)

        # update all ancestor's aggregate values
        for p in reversed(self.ancestors):
            p.agg_r = max(p.agg_r, p.r)
            p.agg_seens += delta_seens

    def reset_inner(self):
        if self.is_leaf():
            self.agg_r = self.r
            self.agg_seens = self.seens
            return self

        self.all_seens = self.seens
        self.all_r = self.r
        for c in self.children():
            self.agg_seens += c.agg_seens
            self.agg_r = max(self.agg_r, c.agg_r)
        return self

    def bonus(self, alpha=1.0):
        p = self.parent
        effective_parent = p.agg_seens
        effective_seen = self.agg_seens
        if effective_seen <= 0.0:
            effective_seen = 1.0
            effective_parent = len(self.children)
        return self.agg_r + math.sqrt(alpha*math.log(effective_parent)/(effective_seen))


def create_tree(num_nodes=10000):
    nodes = []
    queue = deque()
    id = 0
    root = ExNode(str(id), parent=None)
    queue.append(root)
    nodes.append(root)

    while queue:
        parent_node = queue.popleft()
        for i in range(10):
            id += 1
            cur_node = ExNode(str(id), parent=parent_node)
            queue.append(cur_node)
            nodes.append(cur_node)
        if id > num_nodes:
            break
    return root, nodes


def initialize(nodes):
    count = 0
    for i in range(len(nodes)-1, -1, -1):
        leaf = nodes[i]
        count +=1
        leaf.inc_update(0.0)


def get_leaf_nodes(nodes):
    return [n for n in nodes if n.is_leaf]


def generate_rate_from_leaf(t, p, decay=0.95):
    r = {}
    while t >= 1:
        r[t] = p
        p *= decay
        t //= 10
    return r


#let us set up topic click rate configuration
def generate_topic_rate():
    topic_rates = {
        3000: 0.04,
        5000: 0.05,
        7000: 0.04,
    }
    r = {}
    for t, p in topic_rates.items():
        r.update(generate_rate_from_leaf(t, p))
    return r


num_topics = 10000
root, nodes = create_tree(num_nodes=num_topics)
# initialize(nodes)
# print(RenderTree(root))
print(nodes[1].bonus())

#let us set a fix seed
np.random.seed(123)

topic_rates = generate_topic_rate()
print('AAA', topic_rates)

env = BanditEnv(topic_rates, default_rate=0.02, num_topics=num_topics)

docs = np.random.randint(0, 10**7, size=100)
print(docs)
print(env.generate_reward(docs))






