from enum import Enum


class Steps(Enum):
    left = 0
    right = 1


class Node:
    def __init__(self, curr_allocation: list, valuations: list, steps: list, dad=None):
        self.curr_allocation = curr_allocation
        self.right = None
        self.left = None
        self.dad = dad
        self.steps = steps

        if curr_allocation[0] != len(valuations[0]):
            left_allocation = curr_allocation.copy()
            left_allocation[1] *= valuations[0][curr_allocation[0]]

            right_allocation = curr_allocation.copy()
            right_allocation[2] *= valuations[1][curr_allocation[0]]

            left_allocation[0] += 1
            left_steps = self.steps.copy()
            left_steps.append(Steps.left)

            self.left = Node(left_allocation, valuations, left_steps, self)

            right_allocation[0] += 1
            right_steps = self.steps.copy()
            right_steps.append(Steps.right)

            self.right = Node(right_allocation, valuations, right_steps, self)


class BT:
    def __init__(self, valuations):
        self.root = Node([0, 1, 1], valuations, [])

    def iterate_nodes(self, node, callback):
        if node:
            self.iterate_nodes(node.left, callback)
            callback(node)
            self.iterate_nodes(node.right, callback)


def multi_egalitarian_allocation(valuations):
    space = BT(valuations)
    max_min_node = [None]

    def check_min_allocation(node):
        if max_min_node[0] is None or min(node.curr_allocation[1:]) > min(max_min_node[0].curr_allocation[1:]):
            max_min_node[0] = node

    space.iterate_nodes(space.root, check_min_allocation)

    left_results = []
    right_results = []

    left_value = 1
    right_value = 1

    for i in range(len(max_min_node[0].steps)):
        if max_min_node[0].steps[i] is Steps.left:
            left_results.append(i)
            left_value *= valuations[0][i]
        else:
            right_results.append(i)
            right_value *= valuations[1][i]

    print(f"Player 0 gets items {left_results} with value {left_value}")
    print(f"Player 1 gets items {right_results} with value {right_value}")


if __name__ == '__main__':
    valuations = tuple(([4, 5, 6, 7, 8], [8, 7, 6, 5, 4]))

    multi_egalitarian_allocation(valuations)
