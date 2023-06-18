import random
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

class Game:
    def __init__(self, levels):

        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions):

        current_level = self.levels[self.current_level_index]
        steps = 0
        max_success_len = 0
        max_success_len_mashrum = 0
        mashrum_score = 0
        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            if current_step == '_':
                steps += 1
            elif current_step == 'G' and actions[i - 1] == '1':
                steps += 1
            elif current_step == 'L' and actions[i - 1] == '2':
                steps += 1
            elif current_step == 'M' and actions[i - 1] == '0':
                steps += 1
                mashrum_score += 1
            else:
                max_success_len = max(max_success_len, steps)
                steps = 0
                max_success_len_mashrum = mashrum_score
                mashrum_score = 0

        max_success_len = max(max_success_len, steps)
        if self.current_level_len - 1 == max_success_len:
            max_success_len += 5
        return max_success_len == self.current_level_len - 1, max_success_len + max_success_len_mashrum


g = Game(["__M_G__MM_", "_M_G_M_M_L_"])
g.load_next_level()

# This outputs (False, 4)
print(g.get_score("0000000000"))

initial_pop = []
parents = []
children = []
avg = []


def get_avg():
    avgg = sum(pair[1] for pair in parents) / len(parents)
    avg.append(avgg)
    return avgg


def population(size, length):
    for i in range(size):
        string = ""
        for i in range(length - 1):
            string = string + str(random.randint(0, 2))
        initial_pop.append((string, 0))


population(200, 10)
for i in range(200):
    end, sc = g.get_score(initial_pop[i][0])
    initial_pop[i] = (initial_pop[i][0], sc)


def get_parent():
    sorted_pairs = sorted(initial_pop, key=lambda x: x[1], reverse=True)
    return [pair for pair in sorted_pairs[:50]]


parents = get_parent()
get_avg()


def get_child():
    i = 0
    while i < 49:
        p1 = i
        p2 = i + 1
        i += 2
        string1 = parents[p1][0]
        string2 = parents[p2][0]
        cross_point = len(string1) // 2
        child1 = string1[:cross_point] + string2[cross_point:]
        child2 = string1[cross_point:] + string2[:cross_point]
        children.append((child1, 0))
        children.append((child2, 0))
    # for x in range(50):
    #     print(children[x])


get_child()


def evaluate_childs():
    for i in range(len(children)):
        end, sc = g.get_score(children[i][0])
        children[i] = (children[i][0], sc)


evaluate_childs()
for x in range(50):
    print(children[x])


def remainders():
    all = children + parents
    sorted_pairs = sorted(all, key=lambda x: x[1], reverse=True)
    return [pair for pair in sorted_pairs[:50]]

parents = remainders()
get_avg()




get_child()
evaluate_childs()
parents = remainders()
get_avg()


get_child()
evaluate_childs()
parents = remainders()
get_avg()

get_child()
evaluate_childs()
parents = remainders()
get_avg()



for i in range(len(avg)):
    print(avg[i])


fig, ax = plt.subplots()  # Create a figure containing a single axes.
ax.plot([i for i in range(len(avg))], avg)  # Plot some data on the axes.
plt.show()