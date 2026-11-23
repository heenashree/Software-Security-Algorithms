# THis is Multiple Intheritanc Order MRO problem which Pythoin solves iwth stack
from collections import defaultdict
def can_finish(num_courses: int, prerequisites: list[list[int]]) -> bool:
    graph = defaultdict(list)
    for course, prereq in prerequisites:
        graph[course].append(prereq)
    # iterative apprach
    UNVISITED = 0
    VISTING = 1
    VISTED = 2
    states = [UNVISITED]*num_courses

    for start in range(num_courses):
        if states[start] != UNVISITED: continue #stack = [0] - remember the courses are index here so its fine.
        stack = [start]
        while stack:
            node = stack[-1]

            if states[node] == UNVISITED:
                states[node] = VISTING
                for nei in graph[node]:
                    if states[nei] == VISTING:
                        return False
                    elif states[nei] == UNVISITED:
                        stack.append(nei)
            else:
                states[node] = VISTED
                stack.pop()
    return True

def test_can_finish():
    assert can_finish(1,[]) is True
    assert can_finish(3, []) is True
    assert can_finish(2, [[1, 0]]) is True
    assert can_finish(4, [[0, 1], [0, 2], [1, 3], [2, 3]]) is True  # Diamond
    assert can_finish(4, [[1, 0], [3, 2]]) is True  # Disconnected valid
    assert can_finish(2, [[0,1],[1,0]]) is False
    assert can_finish(4, [[0, 1], [0, 2],[1,3],[2,3]]) is True
    assert can_finish(2, [[0, 0]]) is False

    print("All tests passed!")



test_can_finish()