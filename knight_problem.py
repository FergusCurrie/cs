"""Keyboard Knights of Acacia Solution. 

1. Construct graph where nodes are keys, links are to keys which are valid knight moves
2. Recursively search graph for all possible paths of length 10
3. Maintain a table mapping state (node, length of sequence, vowel count) to number of paths
"""

import numpy as np

KEYBOARD = [
    ["A", "B", "C", "D", "E"],
    ["F", "G", "H", "I", "J"],
    ["K", "L", "M", "N", "O"],
    ["", "1", "2", "3", ""],
]

KNIGHT_MOVES = [
    (-2, -1),
    (-2, 1),
    (-1, -2),
    (-1, 2),
    (1, -2),
    (1, 2),
    (2, -1),
    (2, 1),
]


class KeyNode:
    def __init__(self, key: str):
        self.key = key
        self.knight_neighbours = []

    def __str__(self) -> str:
        return f"{self.key} -> {[x.key for x in self.knight_neighbours]}"


class KeyboardGraph:
    def __init__(self, keyboard: list):
        self.nodes = {}
        self.keyboard = keyboard
        self.construct_graph()

    def get_valid_knight_moves(self, target_key: str) -> list:
        """Find valid knight moves from a given key.

        Args:
            target_key : Key to move from

        Returns:
            list: List of keys that are valid knight moves
        """
        # Find index of key on keyboard
        for i, row in enumerate(self.keyboard):
            for j, key in enumerate(row):
                if target_key == key:
                    row_index, col_index = i, j

        # Find valid knight moves from key
        valid_moves = []
        for row_change, col_change in KNIGHT_MOVES:
            new_row = row_index + row_change
            new_col = col_index + col_change
            if self.check_valid_key_index(new_row, new_col):
                valid_moves.append(self.keyboard[new_row][new_col])
        return valid_moves

    def check_valid_key_index(self, row_index: int, col_index: int) -> bool:
        # Check move valid index on row
        if row_index < 0 or row_index >= len(self.keyboard):
            return False
        # Check move valid index on col
        if col_index < 0 or col_index >= len(self.keyboard[row_index]):
            return False
        # Check move not moving to empty key
        if self.keyboard[row_index][col_index] == "":
            return False
        return True

    def construct_graph(self) -> None:
        """Construct graph from keyboard. Graph links KeyNodes to neighbouring KeyNodes (valid knight moves)"""
        # First construct nodes (keys on keyboard)
        for row in self.keyboard:
            for key in row:
                if key != "":
                    self.nodes[key] = KeyNode(key=key)

        # Add edges (valid horse moves to other keys)
        for row in self.keyboard:
            for key in row:
                if key != "":
                    valid_moves = self.get_valid_knight_moves(key)
                    for move in valid_moves:
                        self.nodes[key].knight_neighbours.append(self.nodes[move])

    def get_node_index(self, node: KeyNode) -> list:
        return list(self.nodes.keys()).index(node.key)


class KnightSolver:
    def __init__(self, graph: KeyboardGraph, max_vowels: int, length: int = 10) -> None:
        self.move_count_lookup = np.zeros(
            (len(graph.nodes.keys()), length - 1, max_vowels + 1)
        )
        self.max_vowels = max_vowels
        self.graph = graph
        self.length = length

    def solve(self) -> int:
        """Calculate number of sequences for each starting point and sum.

        Returns:
            int : total number of sequences
        """
        total_count = 0
        for node in self.graph.nodes.values():
            vowel_count = 1 if node.key.upper() in ["A", "E", "I", "O", "U"] else 0
            total_count += self.recursive_search(
                node, vowel_count=vowel_count, current_sequence=""
            )
        return total_count

    def recursive_search(
        self, current_key_node: KeyNode, vowel_count: int, current_sequence: str
    ) -> int:
        """For a given state (current key, length of sequence, number of vowels) recursively
        search all possible paths, returning a count.

        To avoid recalculating the same path multiple times, a lookup table from state
        (current key, length of sequence, number of vowels) to count is maintained.

        Args:
            current_key_node (Node): Current key node in graph.
            vowel_count (int, optional): Number of vowels in sequence.
            current_sequence (str, optional): Current sequence.

        Returns:
            int : count of sequences
        """
        # add current key to sequence, return count if sequence complete
        current_sequence += current_key_node.key
        if len(current_sequence) == self.length:
            return 1

        # check lookup table
        if (
            self.move_count_lookup[
                self.graph.get_node_index(current_key_node),
                len(current_sequence) - 1,
                vowel_count,
            ]
            != 0
        ):
            return self.move_count_lookup[
                self.graph.get_node_index(current_key_node),
                len(current_sequence) - 1,
                vowel_count,
            ]

        # recursively search all neighbours (valid knight moves). check vowel count.
        count = 0
        for neighbour in current_key_node.knight_neighbours:
            next_num_vowles = vowel_count
            if neighbour.key.upper() in ["A", "E", "I", "O", "U"]:
                next_num_vowles += 1
            if next_num_vowles > self.max_vowels:
                continue
            count += self.recursive_search(neighbour, next_num_vowles, current_sequence)

        # update lookup table
        self.move_count_lookup[
            self.graph.get_node_index(current_key_node),
            len(current_sequence) - 1,
            vowel_count,
        ] = count
        return int(count)


if __name__ == "__main__":
    graph = KeyboardGraph(KEYBOARD)
    for graph_node in graph.nodes.values():
        print(graph_node)
    solver = KnightSolver(graph, max_vowels=2)
    count = solver.solve()
    print(f"{count}")
