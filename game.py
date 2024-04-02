import random
from enum import Enum
import matplotlib.pyplot as plt

from animation2 import Game


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
                 mutation_probabilty=0.1, iteration_num=5, level="", selection_size=50, crossover_probability=0.8):
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
        self.score_set = []
        self.selection_size = selection_size
        self.level = level
        self.level_len = len(level)
        self.crossover_prbability = crossover_probability
        self.max_value=[]
        self.min_value = []

    def get_score(self, actions):
        current_level = self.level
        steps = 0
        max_success_len = 0
        max_success_len_mashrum = 0
        mashrum_score = 0
        scores = 0
        if actions[self.level_len - 3] == '1':
            scores = scores + 1
        for i in range(self.level_len - 1):
            current_step = current_level[i]
            if actions[i] == '1' and actions[i + 1] in {'1', '2'}:
                scores -= 3
            if current_step == '_':
                steps += 1
            elif current_step == 'G' and actions[i - 1] == '1':
                steps += 1
            elif current_step == 'G' and actions[i - 2] == '1':
                steps += 1
                scores += 2
            elif current_step == 'L' and actions[i - 1] == '2':
                steps += 1
            elif current_step == 'M' and actions[i - 1] == '0':
                steps += 1
                mashrum_score += 1
            else:
                scores -= 2
                max_success_len = max(max_success_len, steps)
                steps = 0
                max_success_len_mashrum = mashrum_score
                mashrum_score = 0

        max_success_len = max(max_success_len, steps)
        if self.evaluation_type == EvaluationType.WITH_WIN_SCORE:
            if self.level_len - 1 == max_success_len:
                max_success_len += 6

        return max_success_len == self.level_len - 1, max_success_len + max_success_len_mashrum + scores

    def get_average(self):
        average = sum(pair[1] for pair in self.parents) / len(self.parents)
        self.average_for_iterations.append(average)
        return average

    def initial_population(self):
        for i in range(self.initial_population_size):
            string = ""
            for i in range(self.level_len):
                string = string + str(random.randint(0, 2))
            self.population.append((string, 0))

    def select_parent(self):

        if self.selection_type == SelectionType.BEST:
            sorted_population = sorted(self.population, key=lambda x: x[1], reverse=True)
            self.parents = [pair for pair in sorted_population[:self.selection_size]]

        if self.selection_type == SelectionType.ROULLETE_WHEEL:
            self.parents = []
            min_val = min(self.population, key=lambda z: z[1])
            if min_val[1] < 0:
                weights = [pair[1]-min_val[1]+1 for pair in self.population]
            else:
                weights = [pair[1] for pair in self.population]
            total_weight = sum(weights)
            probabilities = [weight / total_weight for weight in weights]
            cumulative_probs = [sum(probabilities[:i + 1]) for i in range(len(probabilities))]
            for i in range(self.selection_size):
                rand_num = random.uniform(0, 1)
                index = 0
                for i, prob in enumerate(cumulative_probs):
                    if rand_num <= prob:
                        index = i
                        break
                self.parents.append(self.population[index])


                # selected_value = random.choices(self.population, probabilities)[0]

    def evaluate(self):
        for i in range(len(self.population)):
            # print(self.population[i][0],i)
            end, sc = self.get_score(self.population[i][0])
            self.population[i] = (self.population[i][0], sc)
            self.score_set.append(sc)

    def crossover(self):
        i = 0
        if self.crossover_type == CrossoverType.SINGLE_POINT:
            while i < self.selection_size:
                p1, p2 = i, i + 1
                i += 2
                if random.uniform(0, 1) < self.crossover_prbability:
                    string1, string2 = self.parents[p1][0], self.parents[p2][0]
                    cross_point = len(string1) // 2
                    child1 = string1[:cross_point] + string2[cross_point:]
                    child2 = string1[cross_point:] + string2[:cross_point]
                    self.children.append((child1, 0))
                    self.children.append((child2, 0))

        if self.crossover_type == CrossoverType.TWO_POINT:
            while i < self.selection_size:
                p1, p2 = i, i + 1
                i += 2
                if random.uniform(0, 1) < self.crossover_prbability:
                    string1, string2 = self.parents[p1][0], self.parents[p2][0]
                    cross_point = len(string1) // 3
                    child1 = string1[:cross_point] + string2[cross_point:2 * cross_point] + string1[cross_point * 2:]
                    child2 = string2[:cross_point] + string1[cross_point:2 * cross_point] + string2[cross_point * 2:]
                    self.children.append((child1, 0))
                    self.children.append((child2, 0))

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
        print(self.population)
        self.evaluate()
        for i in range(self.iteration_num):
            print("it ",i)
            self.select_parent()
            self.crossover()
            self.mutaion()
            self.next_population()
            self.max_value.append(max(self.population, key=lambda z: z[1])[1])
            self.min_value.append(min(self.population, key=lambda z: z[1])[1])
            self.evaluate()
            self.get_average()
        print(max(self.population, key=lambda x: x[1]))
        self.show_result()

    def show_result(self):
        fig, ax = plt.subplots()
        ax.plot([i for i in range(1, len(self.average_for_iterations) + 1)],
                self.average_for_iterations)
        plt.show()
        generations = range(1, len(self.max_value) + 1)

        plt.plot(generations, self.max_value, label='Max Value')
        plt.plot(generations,self.min_value, label='Min Value')
        plt.xlabel('Generation')
        plt.ylabel('Value')
        plt.title('Max and Min Values in Each Generation')
        plt.legend()
        plt.show()
        game = Game(self.level, max(self.population, key=lambda x: x[1])[0])
        game.run()
        # self.show_animation()


def read_file(filename):
    with open(filename, 'r') as file:
        content = file.read()
    return content


# Example usage
level_num = 8

file_path = "levels/level" + str(level_num) + ".txt"
level = read_file(file_path)
evoloutioanry_algorithm = EA(500, EvaluationType.WITH_WIN_SCORE, SelectionType.ROULLETE_WHEEL, CrossoverType.TWO_POINT, 0.5, 200,
                             level, 100, 0.9)
evoloutioanry_algorithm.run_algorithm()
