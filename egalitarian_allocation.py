import random
import time
from enum import Enum
import  matplotlib.pyplot as plt


class Steps(Enum):
    left = 0
    right = 1


class Choice(Enum):
    nothing = 0
    first_rule = 1
    second_rule = 2
    both_rules = 3


class Node:
    def __init__(self, curr_allocation: list, valuations: list, steps: list, choise: Choice, prev_alloc: set, dad=None):
        self.curr_allocation = curr_allocation
        self.right = None
        self.left = None
        self.dad = dad
        self.steps = steps


        if curr_allocation[0] != len(valuations[0]):

            if choise in [Choice.second_rule, Choice.both_rules]:
                rand = curr_allocation.copy()[1:]
                optimal = curr_allocation.copy()[1:]
                for i in range(curr_allocation[0], len(valuations[0])):
                    optimal[0] += valuations[0][i]
                    optimal[1] += valuations[1][i]
                    rand_coin = random.choice([0, 1])
                    if rand_coin == 0:
                        rand[0] += valuations[0][i]
                    else:
                        rand[1] += valuations[1][i]
                if min(rand) > min(optimal):
                    return

            left_allocation = curr_allocation.copy()
            left_allocation[1] += valuations[0][curr_allocation[0]]

            right_allocation = curr_allocation.copy()
            right_allocation[2] += valuations[1][curr_allocation[0]]

            if choise in [Choice.first_rule, Choice.both_rules]:
                if tuple(left_allocation) in prev_alloc:
                    return
                if tuple(right_allocation) in prev_alloc:
                    return

            left_allocation[0] += 1
            left_steps = self.steps.copy()
            left_steps.append(Steps.left)
            prev_alloc.add(tuple(left_allocation))
            self.left = Node(left_allocation, valuations, left_steps, choise, prev_alloc, self)

            right_allocation[0] += 1
            right_steps = self.steps.copy()
            right_steps.append(Steps.right)
            prev_alloc.add(tuple(right_allocation))
            self.right = Node(right_allocation, valuations, right_steps, choise, prev_alloc, self)


class BT:
    def __init__(self, valuations, choice: Choice):
        self.root = Node([0, 0, 0], valuations, [], choice, set())

    def iterate_nodes(self, node, callback):
        if node:
            self.iterate_nodes(node.left, callback)
            callback(node)
            self.iterate_nodes(node.right, callback)


def egalitarian_allocation(valuations, choice: Choice):

    space = BT(valuations, choice)
    max_min_node = [None]

    def check_min_allocation(node):
        if max_min_node[0] is None or min(node.curr_allocation[1:]) > min(max_min_node[0].curr_allocation[1:]):
            max_min_node[0] = node

    space.iterate_nodes(space.root, check_min_allocation)

    left_results = []
    right_results = []

    left_value = 0
    right_value = 0

    for i in range(len(max_min_node[0].steps)):
        if max_min_node[0].steps[i] is Steps.left:
            left_results.append(i)
            left_value += valuations[0][i]
        else:
            right_results.append(i)
            right_value += valuations[1][i]

    print(f"Player 0 gets items {left_results} with value {left_value}")
    print(f"Player 1 gets items {right_results} with value {right_value}")



if __name__ == '__main__':
    if __name__ == '__main__':
        valuations = ([11, 22, 33], [22, 11, 44])  # Example valuations

        # Lists to store execution times for each choice
        times_nothing = []
        times_first_rule = []
        times_second_rule = []
        times_both_rules = []

        # Run the function for each number of products between 1 and 30
        for num_products in range(1, 31):
            valuations = ([random.randint(1, 50) for _ in range(num_products)],
                          [random.randint(1, 50) for _ in range(num_products)])

            # Run the function for each choice and measure execution time
            for choice in Choice:
                start_time = time.time()
                egalitarian_allocation(valuations, choice)
                end_time = time.time()
                execution_time = end_time - start_time

                # Append the execution time to the corresponding list
                if choice == Choice.nothing:
                    times_nothing.append(execution_time)
                elif choice == Choice.first_rule:
                    times_first_rule.append(execution_time)
                elif choice == Choice.second_rule:
                    times_second_rule.append(execution_time)
                elif choice == Choice.both_rules:
                    times_both_rules.append(execution_time)

        # Plot the results
        plt.plot(range(1, 31), times_nothing, label='Nothing')
        plt.plot(range(1, 31), times_first_rule, label='First Rule')
        plt.plot(range(1, 31), times_second_rule, label='Second Rule')
        plt.plot(range(1, 31), times_both_rules, label='Both Rules')

        plt.xlabel('Number of Products')
        plt.ylabel('Execution Time (seconds)')
        plt.title('Execution Time for Different Choices')
        plt.legend()
        plt.show()