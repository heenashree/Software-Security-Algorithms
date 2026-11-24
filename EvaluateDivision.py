from collections import defaultdict
from typing import List


class Solution:
    def calcEquation(self, equations: List[List[str]], values: List[float], queries: List[List[str]]) -> List[float]:
        graph = defaultdict(list)  # bidirectional graph
        for (src, dst), rate in zip(equations, values):  # we use both equatiosn and values and create graph
            graph[src].append((dst, rate))
            graph[dst].append(
                (src, 1.0 / rate))  # we are doing bidirectiiona and if a->b then to get to b->a it has to inverse

        # once graph is created we start traversing graph
        def dfs(curr, target, visited):
            if curr == target:  # currnt is b and target is also b
                return 1.0
            visited.add(curr)  # oterhwsie we add visited i.e b to seen set of list so we dont visit it again
            for nei, rate in graph[curr]:
                if nei not in visited:
                    sub_result = dfs(nei, target, visited)  # we loop over nei to ask if they can reach the target
                    if sub_result != -1.0:
                        return rate * sub_result
            return -1.0

        res = []
        for start, end in queries:
            if start not in graph or end not in graph:
                results.append(-1.0)
            else:
                results.append(dfs(start, end, set()))

