import pytest
from knight_problem import KeyNode, KnightSolver, KeyboardGraph


def test_impossible_knight_problem():
    keyboard = [
        ["A", "B"],
        ["F", "G"],
    ]
    graph = KeyboardGraph(keyboard)
    solver = KnightSolver(graph, max_vowels=2)
    assert solver.solve() == 0


def test_mini_knight_problem():
    keyboard = [
        ["1", "2", "3"],
        ["4", "5", "6"],
        ["7", "8", "9"],
    ]
    graph = KeyboardGraph(keyboard)
    solver = KnightSolver(graph, max_vowels=2)
    assert solver.solve() == 2**9 * 8


def test_vowels():
    keyboard1 = [
        ["1", "2", "3"],
        ["4", "5", "6"],
    ]
    graph = KeyboardGraph(keyboard1)
    solver = KnightSolver(graph, max_vowels=2)
    assert solver.solve() == 4
    keyboard2 = [
        ["A", "2", "3"],
        ["4", "5", "6"],
    ]
    graph = KeyboardGraph(keyboard2)
    solver = KnightSolver(graph, max_vowels=4)
    assert solver.solve() == 2
    solver = KnightSolver(graph, max_vowels=5)
    assert solver.solve() == 4


def test_one_path():
    keyboard1 = [
        ["", "", "", "", "", ""],
        ["", "", "2", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "3", "", "", "", ""],
        ["", "", "", "", "", ""],
        ["", "", "", "", "", ""],
    ]
    graph = KeyboardGraph(keyboard1)
    solver = KnightSolver(graph, max_vowels=0)
    assert solver.solve() == 2


def test_diamond():
    keyboard1 = [[""]]
    graph = KeyboardGraph(keyboard=keyboard1)
    graph.nodes = {
        "A": KeyNode("A"),
        "1": KeyNode("1"),
        "2": KeyNode("2"),
    }
    graph.nodes["A"].knight_neighbours = [graph.nodes["1"], graph.nodes["2"]]
    graph.nodes["1"].knight_neighbours = [graph.nodes["A"], graph.nodes["2"]]
    graph.nodes["2"].knight_neighbours = [graph.nodes["A"], graph.nodes["1"]]
    solver = KnightSolver(graph, max_vowels=1, length=2)
    assert solver.solve() == 6
    solver = KnightSolver(graph, max_vowels=1, length=3)
    assert solver.solve() == 10
    solver = KnightSolver(graph, max_vowels=1, length=4)
    assert solver.solve() == 14
    solver = KnightSolver(graph, max_vowels=1, length=5)
    assert solver.solve() == 18
