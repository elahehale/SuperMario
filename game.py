import random
from enum import Enum

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


levels = []
for i in range(1, 10):
    with open("levels/level" + str(i) + ".txt", "r") as file:
        levels.append(file.read())

g = Game(["___M__L_M_G__MM_", "_M_G_M_M_L_"])
g.load_next_level()


class EvaluationType(Enum):
    WITH_WIN_SCORE = 1
    NO_WIN_SCORE = 2


class SelectionType(Enum):
    BEST = 1
    ROULLETE_WHEEL = 2


class CrossoverType(Enum):
    SINGLE_POINT = 1
    TWO_POINT = 1


class EA:

    def __init__(self, initial_population_size=500, evaluation_type=EvaluationType.WITH_WIN_SCORE
                 , selection_type=SelectionType.BEST, crossover_type=CrossoverType.SINGLE_POINT,
                 mutation_probabilty=0.1, iteration_num=5, game_roud_length=10, selection_size=50):
        self.initial_population_size = initial_population_size
        self.evaluation_type = evaluation_type
        self.selection_type = selection_type
        self.crossover_type = crossover_type
        self.mutation_probability = mutation_probabilty
        self.iteration_num = iteration_num
        self.population = []
        self.average_for_iterations = []
        self.children = []
        self.parents = []
        self.game_roud_length = game_roud_length
        self.score_set = []
        self.selection_size = selection_size

    def get_average(self):
        average = sum(pair[1] for pair in self.parents) / len(self.parents)
        self.average_for_iterations.append(average)
        return average

    def initial_population(self):
        for i in range(self.initial_population_size):
            string = ""
            for i in range(self.game_roud_length):
                string = string + str(random.randint(0, 2))
            self.population.append((string, 0))

    def select_parent(self):

        if self.selection_type == SelectionType.BEST:
            sorted_population = sorted(self.population, key=lambda x: x[1], reverse=True)
            self.parents = [pair for pair in sorted_population[:self.selection_size]]

        if self.selection_type == SelectionType.ROULLETE_WHEEL:
            self.parents = []
            weights = [pair[1] for pair in self.population]
            total_weight = sum(weights)
            probabilities = [weight / total_weight for weight in weights]
            for i in range(self.selection_size):
                selected_value = random.choices(self.population, probabilities)[0]
                self.parents.append(selected_value)

    def evaluate(self):
        for i in range(len(self.population)):
            # print(self.population[i][0],i)
            end, sc = g.get_score(self.population[i][0])
            self.population[i] = (self.population[i][0], sc)
            self.score_set.append(sc)

    def crossover(self):
        i = 0
        if self.crossover_type == CrossoverType.SINGLE_POINT:
            while i < self.selection_size:
                p1, p2 = i, i + 1
                i += 2
                string1, string2 = self.parents[p1][0], self.parents[p2][0]
                cross_point = len(string1) // 2
                child1 = string1[:cross_point] + string2[cross_point:]
                child2 = string1[cross_point:] + string2[:cross_point]
                self.children.append((child1, 0))
                self.children.append((child2, 0))
                # print('par1',string1,'parent2',string2,'child1',child1)

        if self.crossover_type == CrossoverType.TWO_POINT:
            while i < self.selection_size:
                p1, p2 = i, i + 1
                i += 2
                string1, string2 = self.parents[p1][0], self.parents[p2][0]
                cross_point = len(string1) // 3
                child1 = string1[:cross_point] + string2[cross_point:2 * cross_point] + string1[cross_point * 2:]
                child2 = string2[:cross_point] + string1[cross_point:2 * cross_point] + string2[cross_point * 2:]
                self.children.append((child1, 0))
                self.children.append((child2, 0))
        print(self.children,len(self.children))
    def mutaion(self):
        for i in range(len(self.children)):
            string = self.children[i][0]
            mutated_string = ""
            for char in string:
                if random.uniform(0, 1) < self.mutation_probability:
                    mutated_string += random.choice('012')
                else:
                    mutated_string = mutated_string + str(char)
            self.children[i] = (mutated_string, self.children[i][1])

    def next_population(self):
        self.population = []
        self.population = self.parents + self.children

    def run_algorithm(self):
        self.initial_population()
        self.evaluate()
        print('hello')
        for i in range(self.iteration_num):
            self.select_parent()
            self.crossover()
            self.mutaion()
            self.next_population()
            self.evaluate()
            self.get_average()
        self.show_result()

    def show_result(self):
        fig, ax = plt.subplots()
        ax.plot([i for i in range(1,len(self.average_for_iterations)+1)],
                self.average_for_iterations)
        plt.show()


evoloutioanry_algorithm = EA(500, EvaluationType.WITH_WIN_SCORE, SelectionType.BEST, CrossoverType.SINGLE_POINT, 0.1,5,16,50)
evoloutioanry_algorithm.run_algorithm()

